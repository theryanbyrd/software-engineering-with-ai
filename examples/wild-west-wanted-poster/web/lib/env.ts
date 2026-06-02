// lib/env.ts — Centralized, validated access to environment variables. Ch 34 secrets/config.
// Real values are injected by ECS from AWS Secrets Manager; locally from .env.local.
import { z } from 'zod';

const schema = z.object({
  DATABASE_URL: z.string().url(),
  APP_URL: z.string().url(),
  AWS_REGION: z.string().min(1),
  S3_UPLOAD_BUCKET: z.string().min(1),
  S3_POSTER_BUCKET: z.string().min(1),
  SQS_QUEUE_URL: z.string().url(),
  SES_FROM_EMAIL: z.string().email(),
  STRIPE_SECRET_KEY: z.string().min(1),
  STRIPE_WEBHOOK_SECRET: z.string().min(1),
  STRIPE_PRICE_CREDITS: z.string().min(1),
  GEMINI_API_KEY: z.string().optional().default(''),
  AUTH_SECRET: z.string().min(32, 'AUTH_SECRET must be at least 32 bytes'),
  ADMIN_EMAILS: z.string().optional().default(''),
});

let cached: z.infer<typeof schema> | null = null;

/** Parse + cache process.env once. Throws loudly on misconfiguration at first use. */
export function env(): z.infer<typeof schema> {
  if (cached) return cached;
  const parsed = schema.safeParse(process.env);
  if (!parsed.success) {
    throw new Error('Invalid environment configuration: ' + parsed.error.message);
  }
  cached = parsed.data;
  return cached;
}

/** Normalized set of admin emails (lowercased) from ADMIN_EMAILS. */
export function adminEmails(): Set<string> {
  return new Set(
    env()
      .ADMIN_EMAILS.split(',')
      .map((e) => e.trim().toLowerCase())
      .filter(Boolean),
  );
}
