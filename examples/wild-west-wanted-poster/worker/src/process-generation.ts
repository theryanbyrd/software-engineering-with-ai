// process-generation.ts — Orchestrates one poster generation job end-to-end.
// Book chapter concept: "The worker owns the saga" — mark processing, fetch input, call the AI,
// composite, store output, mark done, notify. On failure, mark failed AND refund the spent credit
// via a +1 'refund' ledger event (event sourcing: corrections are new events, never edits).

import { PoolClient } from 'pg';
import { query, withTransaction, appendLedger } from './db.js';
import { getObjectBytes, putObjectBytes } from './s3.js';
import { sendPosterReadyEmail } from './ses.js';
import { generateWantedPortrait } from './gemini.js';
import { composePoster, randomReward } from './poster.js';

/** Shape of a generation job message pulled from SQS. */
export interface GenerationJob {
  genId: string;
  userId: string;
  uploadKey: string;
}

const UPLOAD_BUCKET = requiredEnv('S3_UPLOAD_BUCKET');
const POSTER_BUCKET = requiredEnv('S3_POSTER_BUCKET');

function requiredEnv(name: string): string {
  const v = process.env[name];
  if (!v) throw new Error(`${name} is required`);
  return v;
}

interface GenerationRow {
  id: string;
  user_id: string;
  status: string;
  upload_key: string | null;
}

interface UserRow {
  email: string;
  display_name: string;
}

/** Transition a generation to a new status (with optional error/poster_key). */
async function setStatus(
  genId: string,
  status: 'processing' | 'done' | 'failed',
  fields: { posterKey?: string; error?: string } = {},
): Promise<void> {
  await query(
    `UPDATE generations
        SET status = $2,
            poster_key = COALESCE($3, poster_key),
            error = $4,
            updated_at = now()
      WHERE id = $1`,
    [genId, status, fields.posterKey ?? null, fields.error ?? null],
  );
}

/**
 * Refund the single credit spent at upload time. Idempotency note: we tag the refund with the
 * generation id in `ref`, so we check for an existing refund before inserting if the same job is
 * ever reprocessed after a partial failure.
 */
async function refundCredit(userId: string, genId: string): Promise<void> {
  await withTransaction(async (client: PoolClient) => {
    const existing = await client.query(
      `SELECT 1 FROM credit_ledger WHERE reason = 'refund' AND ref = $1 LIMIT 1`,
      [genId],
    );
    if (existing.rowCount && existing.rowCount > 0) return; // already refunded
    await appendLedger(client, userId, +1, 'refund', genId);
  });
}

/**
 * Process a single generation job. Throws on failure AFTER recording failed status + refund,
 * so the caller can decide whether to delete the SQS message or let it hit the DLQ.
 */
export async function processGeneration(job: GenerationJob): Promise<void> {
  const { genId, userId, uploadKey } = job;

  // Load the generation + user. If the row is missing, there's nothing to do (drop the message).
  const rows = await query<GenerationRow>(
    `SELECT id, user_id, status, upload_key FROM generations WHERE id = $1`,
    [genId],
  );
  const gen = rows[0];
  if (!gen) {
    console.warn(`[process] generation ${genId} not found; dropping message`);
    return;
  }
  if (gen.status === 'done') {
    console.log(`[process] generation ${genId} already done; skipping`);
    return;
  }

  const userRows = await query<UserRow>(
    // Use the local part of the email as a friendly default display name.
    `SELECT email, split_part(email, '@', 1) AS display_name FROM users WHERE id = $1`,
    [userId],
  );
  const user = userRows[0];
  if (!user) {
    console.warn(`[process] user ${userId} not found for generation ${genId}; dropping`);
    return;
  }

  try {
    await setStatus(genId, 'processing');

    const key = uploadKey || gen.upload_key;
    if (!key) throw new Error(`generation ${genId} has no upload key`);

    // 1. Download the user's uploaded portrait from the private uploads bucket.
    const original = await getObjectBytes(UPLOAD_BUCKET, key);

    // 2. Transform it into a sepia Old-West portrait via Gemini.
    const { bytes: portrait } = await generateWantedPortrait(original);

    // 3. Composite the final WANTED poster.
    const posterPng = await composePoster({
      portrait,
      name: user.display_name,
      reward: randomReward(),
    });

    // 4. Store the finished poster in the private posters bucket.
    const posterKey = `posters/${userId}/${genId}.png`;
    await putObjectBytes(POSTER_BUCKET, posterKey, posterPng, 'image/png');

    // 5. Mark done.
    await setStatus(genId, 'done', { posterKey });

    // 6. Notify the user out-of-band (best effort — don't fail the job on email hiccups).
    try {
      await sendPosterReadyEmail(user.email, genId);
    } catch (emailErr) {
      console.error(`[process] poster-ready email failed for ${genId}`, emailErr);
    }

    console.log(`[process] generation ${genId} done -> ${posterKey}`);
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    console.error(`[process] generation ${genId} failed: ${message}`);

    // Record the failure and refund the spent credit so the user isn't charged for our error.
    await setStatus(genId, 'failed', { error: message.slice(0, 1000) });
    try {
      await refundCredit(userId, genId);
    } catch (refundErr) {
      console.error(`[process] refund failed for ${genId}`, refundErr);
    }

    // Re-throw so the consumer leaves the message for redelivery/DLQ per its retry policy.
    throw err;
  }
}
