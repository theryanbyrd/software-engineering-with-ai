// app/auth/verify/route.ts — GET ?token: consume a magic-link token, complete login (first-login
// free credits), set the signed session cookie, then redirect home. Ch 24 session establishment.
import { NextRequest, NextResponse } from 'next/server';
import { query } from '@/lib/db';
import { env } from '@/lib/env';
import { issueSession } from '@/lib/auth';
import { completeLogin } from '@/lib/users';

export const runtime = 'nodejs';

export async function GET(req: NextRequest): Promise<NextResponse> {
  const token = req.nextUrl.searchParams.get('token');
  const appUrl = env().APP_URL;

  if (!token) {
    return NextResponse.redirect(`${appUrl}/auth?error=missing_token`);
  }

  // Atomically consume the token if still valid + unconsumed, returning its user_id.
  const rows = await query<{ user_id: string }>(
    `UPDATE auth_tokens
        SET consumed_at = now()
      WHERE token = $1
        AND consumed_at IS NULL
        AND expires_at > now()
      RETURNING user_id`,
    [token],
  );

  const userId = rows[0]?.user_id;
  if (!userId) {
    return NextResponse.redirect(`${appUrl}/auth?error=invalid_or_expired`);
  }

  const user = await completeLogin(userId);
  await issueSession({ id: user.id, email: user.email, is_admin: user.is_admin });

  return NextResponse.redirect(`${appUrl}/`);
}
