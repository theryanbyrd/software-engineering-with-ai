// lib/http.ts — Tiny helpers to turn thrown errors (AuthError, zod, credits) into JSON Responses.
// Ch 23 API ergonomics. Keeps route handlers terse and consistent.
import { NextResponse } from 'next/server';
import { ZodError } from 'zod';
import { AuthError } from './auth';
import { InsufficientCreditsError } from './credits';

/** Map a caught error to an appropriate JSON NextResponse. */
export function errorResponse(err: unknown): NextResponse {
  if (err instanceof AuthError) {
    return NextResponse.json({ error: err.message }, { status: err.status });
  }
  if (err instanceof InsufficientCreditsError) {
    return NextResponse.json({ error: 'Insufficient credits' }, { status: 402 });
  }
  if (err instanceof ZodError) {
    return NextResponse.json({ error: 'Invalid input', details: err.flatten() }, { status: 400 });
  }
  console.error('Unhandled route error:', err);
  return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
}
