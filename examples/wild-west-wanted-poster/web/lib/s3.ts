// lib/s3.ts — S3 access: store original uploads (private) + presign GETs for finished posters.
// Ch 28 object storage. Both buckets are private; posters are served only via short-lived presigned URLs.
import {
  S3Client,
  PutObjectCommand,
  GetObjectCommand,
} from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';
import { env } from './env';

let client: S3Client | null = null;
function s3(): S3Client {
  if (!client) client = new S3Client({ region: env().AWS_REGION });
  return client;
}

/** Upload bytes to a bucket/key with a content type. Used for original photo uploads. */
export async function putObject(
  bucket: string,
  key: string,
  body: Uint8Array | Buffer,
  contentType: string,
): Promise<void> {
  await s3().send(
    new PutObjectCommand({
      Bucket: bucket,
      Key: key,
      Body: body,
      ContentType: contentType,
    }),
  );
}

/** Generate a presigned GET URL (default 15 min) for a private object. */
export async function presignGet(
  bucket: string,
  key: string,
  expiresInSeconds = 900,
): Promise<string> {
  return getSignedUrl(s3(), new GetObjectCommand({ Bucket: bucket, Key: key }), {
    expiresIn: expiresInSeconds,
  });
}

/** Convenience: store an original upload under uploads/{userId}/{genId}.{ext}. */
export async function putUpload(
  userId: string,
  genId: string,
  body: Uint8Array | Buffer,
  contentType: string,
  ext: string,
): Promise<string> {
  const key = `uploads/${userId}/${genId}.${ext}`;
  await putObject(env().S3_UPLOAD_BUCKET, key, body, contentType);
  return key;
}

/** Convenience: presign a finished poster object key in the posters bucket. */
export async function presignPoster(posterKey: string): Promise<string> {
  return presignGet(env().S3_POSTER_BUCKET, posterKey);
}
