// s3.ts — Thin S3 helper for downloading uploads and storing finished posters.
// Book chapter concept: "Object storage as the durable boundary" — large binaries live in S3,
// the database only holds keys. Buckets are private; the web app serves posters via presigned URLs.

import { S3Client, GetObjectCommand, PutObjectCommand } from '@aws-sdk/client-s3';

const region = process.env.AWS_REGION ?? 'us-west-2';

/** Shared S3 client. */
export const s3 = new S3Client({ region });

/** Read an entire object into a Buffer. Used to fetch the user's uploaded portrait. */
export async function getObjectBytes(bucket: string, key: string): Promise<Buffer> {
  const res = await s3.send(new GetObjectCommand({ Bucket: bucket, Key: key }));
  if (!res.Body) {
    throw new Error(`S3 object ${bucket}/${key} has no body`);
  }
  // Body is a web/node stream depending on runtime; transformToByteArray handles both.
  const bytes = await res.Body.transformToByteArray();
  return Buffer.from(bytes);
}

/** Upload bytes (the composited poster PNG) to the posters bucket. */
export async function putObjectBytes(
  bucket: string,
  key: string,
  body: Buffer,
  contentType: string,
): Promise<void> {
  await s3.send(
    new PutObjectCommand({
      Bucket: bucket,
      Key: key,
      Body: body,
      ContentType: contentType,
    }),
  );
}
