// app/api/auth/request/route.ts — POST {email}: find-or-create the user, mint a magic-link token,
// email it via SES. Ch 24 passwordless auth. Always returns ok to avoid leaking which emails exist.
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { randomUUID } from 'crypto';
import { query } from '@/lib/db';
import { env } from '@/lib/env';
import { sendMagicLink } from '@/lib/ses';
import { findOrCreateUser } from '@/lib/users';
import { errorResponse } from '@/lib/http';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

const Body = z.object({ email: z.string().email() });
const TOKEN_TTL_MINUTES = 15;

export async function POST(req: NextRequest): Promise<NextResponse> {
  try {
    const { email } = Body.parse(await req.json());

    // Create (or fetch) the user up front so auth_tokens.user_id matches the conventions schema.
    const user = await findOrCreateUser(email);

    const token = randomUUID() + randomUUID().replace(/-/g, '');
    const expiresAt = new Date(Date.now() + TOKEN_TTL_MINUTES * 60_000);

    await query(
      'INSERT INTO auth_tokens (token, user_id, expires_at) VALUES ($1, $2, $3)',
      [token, user.id, expiresAt],
    );

    const link = `${env().APP_URL}/auth/verify?token=${encodeURIComponent(token)}`;
    await sendMagicLink(user.email, link);

    return NextResponse.json({ ok: true });
  } catch (err) {
    return errorResponse(err);
  }
}
