// middleware.ts — Lightweight auth gate: redirect unauthenticated visitors away from /admin.
// Ch 24 edge auth. Only checks for presence of the session cookie; full verification happens in handlers.
import { NextRequest, NextResponse } from 'next/server';

const COOKIE_NAME = 'wwwp_session';

export function middleware(req: NextRequest): NextResponse {
  const hasSession = Boolean(req.cookies.get(COOKIE_NAME)?.value);
  if (!hasSession) {
    const url = req.nextUrl.clone();
    url.pathname = '/auth';
    return NextResponse.redirect(url);
  }
  return NextResponse.next();
}

// Guard the admin section at the edge; deep authorization (is_admin) is enforced server-side.
export const config = {
  matcher: ['/admin/:path*'],
};
