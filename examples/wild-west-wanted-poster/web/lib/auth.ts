// lib/auth.ts — Session auth via signed JWT cookie (jose) + helpers to load/guard the current user.
// Ch 24 authn/authz. Magic-link issuance lives in the auth API routes; this owns the session token.
import { cookies } from 'next/headers';
import { SignJWT, jwtVerify } from 'jose';
import { env, adminEmails } from './env';
import { query } from './db';

const COOKIE_NAME = 'wwwp_session';
const SESSION_TTL_SECONDS = 60 * 60 * 24 * 30; // 30 days

export interface SessionUser {
  id: string;
  email: string;
  is_admin: boolean;
}

function secretKey(): Uint8Array {
  return new TextEncoder().encode(env().AUTH_SECRET);
}

/** Sign a JWT for the given user and set it as an httpOnly session cookie. */
export async function issueSession(user: SessionUser): Promise<void> {
  const token = await new SignJWT({ email: user.email, is_admin: user.is_admin })
    .setProtectedHeader({ alg: 'HS256' })
    .setSubject(user.id)
    .setIssuedAt()
    .setExpirationTime(`${SESSION_TTL_SECONDS}s`)
    .sign(secretKey());

  cookies().set(COOKIE_NAME, token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    path: '/',
    maxAge: SESSION_TTL_SECONDS,
  });
}

/** Clear the session cookie (logout). */
export function clearSession(): void {
  cookies().delete(COOKIE_NAME);
}

/** Verify the session cookie and return the user, or null if unauthenticated/invalid. */
export async function getCurrentUser(): Promise<SessionUser | null> {
  const raw = cookies().get(COOKIE_NAME)?.value;
  if (!raw) return null;
  try {
    const { payload } = await jwtVerify(raw, secretKey());
    if (!payload.sub || typeof payload.email !== 'string') return null;
    return {
      id: payload.sub,
      email: payload.email,
      is_admin: payload.is_admin === true,
    };
  } catch {
    return null;
  }
}

/** Require an authenticated user or throw a 401-shaped error. */
export async function requireUser(): Promise<SessionUser> {
  const user = await getCurrentUser();
  if (!user) throw new AuthError('Authentication required', 401);
  return user;
}

/** Require an admin user or throw a 401/403-shaped error. */
export async function requireAdmin(): Promise<SessionUser> {
  const user = await requireUser();
  if (!user.is_admin) throw new AuthError('Admin access required', 403);
  return user;
}

/** True if the email is configured as an admin via ADMIN_EMAILS. */
export function isConfiguredAdmin(email: string): boolean {
  return adminEmails().has(email.trim().toLowerCase());
}

/** Load a user by id from the DB (fresh is_admin etc.). */
export async function loadUser(id: string): Promise<SessionUser | null> {
  const rows = await query<SessionUser>(
    'SELECT id, email, is_admin FROM users WHERE id = $1',
    [id],
  );
  return rows[0] ?? null;
}

/** Typed error carrying an HTTP status so route handlers can map it to a Response. */
export class AuthError extends Error {
  constructor(
    message: string,
    public readonly status: number,
  ) {
    super(message);
    this.name = 'AuthError';
  }
}
