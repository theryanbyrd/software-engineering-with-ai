// app/auth/page.tsx — Magic-link request screen (client). Posts an email to /api/auth/request. Ch 24 auth UI.
'use client';

import { useState } from 'react';

export default function AuthPage() {
  const [email, setEmail] = useState('');
  const [sent, setSent] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const res = await fetch('/api/auth/request', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ email }),
      });
      if (!res.ok) {
        setError('Something went wrong. Please try again.');
        return;
      }
      setSent(true);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main>
      <div className="card">
        {sent ? (
          <div className="notice ok">
            Check your email for a sign-in link. It expires in 15 minutes.
          </div>
        ) : (
          <form onSubmit={submit}>
            <p>Enter your email and we&apos;ll wire you a sign-in link.</p>
            {error ? <div className="notice err">{error}</div> : null}
            <input
              className="field"
              type="email"
              required
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <p>
              <button className="btn" disabled={busy} type="submit">
                {busy ? 'Sending…' : 'Send magic link'}
              </button>
            </p>
          </form>
        )}
      </div>
    </main>
  );
}
