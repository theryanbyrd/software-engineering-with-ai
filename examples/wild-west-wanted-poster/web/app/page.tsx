// app/page.tsx — Home (server component): resolves session, shows balance + recent generations,
// and mounts the client uploader/poller. Ch 13 worked-example main screen.
import Link from 'next/link';
import { getCurrentUser } from '@/lib/auth';
import { getBalance } from '@/lib/credits';
import { query } from '@/lib/db';
import { Uploader } from './uploader';

export const dynamic = 'force-dynamic';

interface RecentGen {
  id: string;
  status: string;
}

export default async function HomePage() {
  const user = await getCurrentUser();

  if (!user) {
    return (
      <main>
        <div className="card">
          <p>Sign in to mint your own Old-West WANTED poster. 5 free posters every month.</p>
          <Link className="btn" href="/auth">
            Sign in to get started
          </Link>
        </div>
      </main>
    );
  }

  const [balance, recent] = await Promise.all([
    getBalance(user.id),
    query<RecentGen>(
      'SELECT id, status FROM generations WHERE user_id = $1 ORDER BY created_at DESC LIMIT 12',
      [user.id],
    ),
  ]);

  return (
    <main>
      <div className="card balance">
        <div>
          <div className="sub">Signed in as {user.email}</div>
          <div>
            Credits: <span className="count">{balance}</span>
          </div>
        </div>
        {user.is_admin ? (
          <Link className="btn secondary" href="/admin">
            Admin
          </Link>
        ) : null}
      </div>

      <Uploader initialBalance={balance} initialGenerations={recent} />
    </main>
  );
}
