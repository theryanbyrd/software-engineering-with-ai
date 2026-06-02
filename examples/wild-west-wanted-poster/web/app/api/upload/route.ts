// app/api/upload/route.ts — POST multipart photo: auth required; transactionally spend 1 credit,
// store original to S3, create generations row, enqueue SQS job. Ch 26 async pipeline entrypoint.
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { requireUser } from '@/lib/auth';
import { spendOneCredit } from '@/lib/credits';
import { putUpload } from '@/lib/s3';
import { enqueueGeneration } from '@/lib/sqs';
import { errorResponse } from '@/lib/http';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

const MAX_BYTES = 10 * 1024 * 1024; // 10 MB
const ALLOWED: Record<string, string> = {
  'image/jpeg': 'jpg',
  'image/png': 'png',
  'image/webp': 'webp',
};

const FileMeta = z.object({
  type: z.string().refine((t) => t in ALLOWED, 'Unsupported image type'),
  size: z.number().int().positive().max(MAX_BYTES, 'File too large (max 10MB)'),
});

export async function POST(req: NextRequest): Promise<NextResponse> {
  try {
    const user = await requireUser();

    const form = await req.formData();
    const file = form.get('photo');
    if (!(file instanceof File)) {
      return NextResponse.json({ error: 'Missing photo' }, { status: 400 });
    }
    FileMeta.parse({ type: file.type, size: file.size });

    const ext = ALLOWED[file.type]!;
    const bytes = Buffer.from(await file.arrayBuffer());

    // Spend 1 credit + create the generations row in a single transaction.
    // The S3 upload happens inside the txn (before commit) so a failed upload rolls back the spend.
    let uploadKey = '';
    const genId = await spendOneCredit(user.id, async (client, gid) => {
      uploadKey = await putUpload(user.id, gid, bytes, file.type, ext);
      await client.query(
        `INSERT INTO generations (id, user_id, status, upload_key, created_at, updated_at)
         VALUES ($1, $2, 'queued', $3, now(), now())`,
        [gid, user.id, uploadKey],
      );
    });

    // Side effect AFTER commit: enqueue the job for the worker.
    await enqueueGeneration({ genId, userId: user.id, uploadKey });

    return NextResponse.json({ id: genId }, { status: 201 });
  } catch (err) {
    return errorResponse(err);
  }
}
