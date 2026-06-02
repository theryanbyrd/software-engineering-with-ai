// app/api/generations/[id]/route.ts — GET status of a generation (+ presigned poster URL when done).
// Ch 26 polling the async result. Only the owner may read their generation.
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { requireUser } from '@/lib/auth';
import { query } from '@/lib/db';
import { presignPoster } from '@/lib/s3';
import { errorResponse } from '@/lib/http';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

const Params = z.object({ id: z.string().uuid() });

interface GenRow {
  id: string;
  status: string;
  poster_key: string | null;
  error: string | null;
}

export async function GET(
  _req: NextRequest,
  { params }: { params: { id: string } },
): Promise<NextResponse> {
  try {
    const user = await requireUser();
    const { id } = Params.parse(params);

    const rows = await query<GenRow>(
      'SELECT id, status, poster_key, error FROM generations WHERE id = $1 AND user_id = $2',
      [id, user.id],
    );
    const gen = rows[0];
    if (!gen) return NextResponse.json({ error: 'Not found' }, { status: 404 });

    const posterUrl =
      gen.status === 'done' && gen.poster_key ? await presignPoster(gen.poster_key) : undefined;

    return NextResponse.json({
      id: gen.id,
      status: gen.status,
      posterUrl,
      error: gen.error ?? undefined,
    });
  } catch (err) {
    return errorResponse(err);
  }
}
