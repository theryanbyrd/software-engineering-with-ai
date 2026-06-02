// index.ts — Long-poll SQS consumer entrypoint for the wwwp worker.
// Book chapter concept: "The queue worker loop" — long-poll, dispatch by message kind, delete on
// success, leave failures for SQS redelivery/DLQ. Two kinds: a generation job {genId,userId,
// uploadKey} and a cron control message {command:'reset-monthly'} from EventBridge Scheduler.
// Includes graceful shutdown and per-message visibility extension for slow AI calls.

import {
  SQSClient,
  ReceiveMessageCommand,
  DeleteMessageCommand,
  ChangeMessageVisibilityCommand,
  type Message,
} from '@aws-sdk/client-sqs';
import { processGeneration, type GenerationJob } from './process-generation.js';
import { runMonthlyReset } from './monthly-reset.js';
import { closePool } from './db.js';

const region = process.env.AWS_REGION ?? 'us-west-2';
const queueUrl = requireEnv('SQS_QUEUE_URL');

const WAIT_TIME_SECONDS = 20; // long poll
const MAX_MESSAGES = 5;
const BASE_VISIBILITY_SECONDS = 60; // initial; we extend for in-flight AI work
const VISIBILITY_EXTEND_SECONDS = 120;

function requireEnv(name: string): string {
  const v = process.env[name];
  if (!v) throw new Error(`${name} is required`);
  return v;
}

const sqs = new SQSClient({ region });

/** Discriminated union of everything the queue can carry. */
type IncomingMessage =
  | ({ command?: never } & GenerationJob)
  | { command: 'reset-monthly' };

let shuttingDown = false;

/** Parse + validate the message body into a known shape, or throw. */
function parseBody(raw: string | undefined): IncomingMessage {
  if (!raw) throw new Error('empty message body');
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch {
    throw new Error('message body is not valid JSON');
  }
  if (typeof parsed !== 'object' || parsed === null) {
    throw new Error('message body is not an object');
  }
  const obj = parsed as Record<string, unknown>;

  if (obj.command === 'reset-monthly') {
    return { command: 'reset-monthly' };
  }

  // Otherwise it must be a generation job.
  const { genId, userId, uploadKey } = obj;
  if (typeof genId !== 'string' || typeof userId !== 'string' || typeof uploadKey !== 'string') {
    throw new Error('generation job requires string genId, userId, uploadKey');
  }
  return { genId, userId, uploadKey };
}

/** Keep a long-running message invisible by periodically extending its visibility timeout. */
function startVisibilityHeartbeat(receiptHandle: string): () => void {
  const timer = setInterval(() => {
    sqs
      .send(
        new ChangeMessageVisibilityCommand({
          QueueUrl: queueUrl,
          ReceiptHandle: receiptHandle,
          VisibilityTimeout: VISIBILITY_EXTEND_SECONDS,
        }),
      )
      .catch((err) => console.error('[sqs] visibility extend failed', err));
  }, (VISIBILITY_EXTEND_SECONDS / 2) * 1000);
  // Don't let the heartbeat keep the process alive on its own.
  if (typeof timer.unref === 'function') timer.unref();
  return () => clearInterval(timer);
}

/** Handle one message: dispatch by kind. Throwing leaves it for redelivery/DLQ. */
async function handleMessage(msg: Message): Promise<void> {
  const body = parseBody(msg.Body);

  if ('command' in body && body.command === 'reset-monthly') {
    console.log('[worker] received reset-monthly command');
    await runMonthlyReset();
    return;
  }

  const job = body as GenerationJob;
  console.log(`[worker] processing generation ${job.genId} for user ${job.userId}`);
  await processGeneration(job);
}

/** Delete a successfully handled message so it isn't redelivered. */
async function deleteMessage(receiptHandle: string): Promise<void> {
  await sqs.send(
    new DeleteMessageCommand({ QueueUrl: queueUrl, ReceiptHandle: receiptHandle }),
  );
}

/** Receive a batch and process each message. */
async function pollOnce(): Promise<void> {
  const res = await sqs.send(
    new ReceiveMessageCommand({
      QueueUrl: queueUrl,
      MaxNumberOfMessages: MAX_MESSAGES,
      WaitTimeSeconds: WAIT_TIME_SECONDS,
      VisibilityTimeout: BASE_VISIBILITY_SECONDS,
    }),
  );

  const messages = res.Messages ?? [];
  if (messages.length === 0) return;

  // Process sequentially to keep memory/concurrency predictable for sharp + Gemini.
  for (const msg of messages) {
    if (!msg.ReceiptHandle) continue;
    const stopHeartbeat = startVisibilityHeartbeat(msg.ReceiptHandle);
    try {
      await handleMessage(msg);
      await deleteMessage(msg.ReceiptHandle);
    } catch (err) {
      // Do NOT delete: SQS will redeliver, and after maxReceiveCount it lands in the DLQ.
      // processGeneration has already marked the generation failed + refunded the credit.
      console.error(`[worker] message ${msg.MessageId} failed; leaving for retry/DLQ`, err);
    } finally {
      stopHeartbeat();
    }
  }
}

/** Main loop: poll until a shutdown signal is received. */
async function main(): Promise<void> {
  console.log(`[worker] starting; long-polling ${queueUrl} in ${region}`);
  while (!shuttingDown) {
    try {
      await pollOnce();
    } catch (err) {
      // Receive-level error (throttling, network). Back off briefly, then continue.
      console.error('[worker] poll error; backing off 5s', err);
      await sleep(5000);
    }
  }
  console.log('[worker] loop exited; closing resources');
  await closePool();
  console.log('[worker] shutdown complete');
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/** Graceful shutdown: stop the loop, let the in-flight message finish (visibility heartbeat). */
function installSignalHandlers(): void {
  const onSignal = (signal: string) => {
    console.log(`[worker] received ${signal}; shutting down gracefully`);
    shuttingDown = true;
  };
  process.on('SIGTERM', () => onSignal('SIGTERM'));
  process.on('SIGINT', () => onSignal('SIGINT'));
}

installSignalHandlers();
main().catch((err) => {
  console.error('[worker] fatal error', err);
  process.exit(1);
});
