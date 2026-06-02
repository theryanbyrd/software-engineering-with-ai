// app/admin/page.tsx — Admin dashboard (server component): totals + recent signups. Gated by requireAdmin.
// Ch 31 admin/ops dashboard. All numbers come straight from the event-sourced tables.
import { redirect } from 'next/navigation';
import { requireAdmin, AuthError } from '@/lib/auth';
import { query } from '@/lib/db';

export const dynamic = 'force-dynamic';

interface StatusCount {
  status: string;
  count: number;
}
interface RecentUser {
  id: string;
  email: string;
  created_at: string;
}

export default async function AdminPage() {
  try {
    await requireAdmin();
  } catch (err) {
    if (err instanceof AuthError) redirect('/auth');
    throw err;
  }

  const [users, gensByStatus, ledger, recent] = await Promise.all([
    query<{ count: number }>('SELECT COUNT(*)::int AS count FROM users'),
    query<StatusCount>(
      'SELECT status, COUNT(*)::int AS count FROM generations GROUP BY status ORDER BY status',
    ),
    query<{ issued: number; spent: number }>(
      `SELECT COALESCE(SUM(delta) FILTER (WHERE delta > 0), 0)::int AS issued,
              COALESCE(-SUM(delta) FILTER (WHERE delta < 0), 0)::int AS spent
         FROM credit_ledger`,
    ),
    query<RecentUser>(
      'SELECT id, email, created_at FROM users ORDER BY created_at DESC LIMIT 10',
    ),
  ]);

  const totalUsers = users[0]?.count ?? 0;
  const issued = ledger[0]?.issued ?? 0;
  const spent = ledger[0]?.spent ?? 0;

  return (
    <main>
      <div className="card balance">
        <div>
          <div className="sub">Total users</div>
          <div className="count">{totalUsers}</div>
        </div>
        <div>
          <div className="sub">Credits issued</div>
          <div className="count">{issued}</div>
        </div>
        <div>
          <div className="sub">Credits spent</div>
          <div className="count">{spent}</div>
        </div>
      </div>

      <div className="card">
        <h3>Generations by status</h3>
        <table>
          <thead>
            <tr>
              <th>Status</th>
              <th>Count</th>
            </tr>
          </thead>
          <tbody>
            {gensByStatus.length === 0 ? (
              <tr>
                <td colSpan={2} className="sub">
                  No generations yet
                </td>
              </tr>
            ) : (
              gensByStatus.map((s) => (
                <tr key={s.status}>
                  <td>{s.status}</td>
                  <td>{s.count}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="card">
        <h3>Recent signups</h3>
        <table>
          <thead>
            <tr>
              <th>Email</th>
              <th>Joined</th>
            </tr>
          </thead>
          <tbody>
            {recent.map((u) => (
              <tr key={u.id}>
                <td>{u.email}</td>
                <td>{new Date(u.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
