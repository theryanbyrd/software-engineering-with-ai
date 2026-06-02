// app/uploader.tsx — Client component: drag/drop upload, "Buy 10 credits for \$1", and polling of
// recent generations until done/failed. Ch 26 polling UX over the async pipeline.
'use client';

import { useCallback, useEffect, useRef, useState } from 'react';

interface Gen {
  id: string;
  status: string;
  posterUrl?: string;
  error?: string;
}

const TERMINAL = new Set(['done', 'failed']);

export function Uploader({
  initialBalance,
  initialGenerations,
}: {
  initialBalance: number;
  initialGenerations: { id: string; status: string }[];
}) {
  const [balance, setBalance] = useState(initialBalance);
  const [gens, setGens] = useState<Gen[]>(initialGenerations);
  const [drag, setDrag] = useState(false);
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState<{ kind: 'ok' | 'err'; text: string } | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const refreshBalance = useCallback(async () => {
    const res = await fetch('/api/credits');
    if (res.ok) setBalance((await res.json()).balance);
  }, []);

  // Poll any non-terminal generations every 3s.
  useEffect(() => {
    const pending = gens.filter((g) => !TERMINAL.has(g.status));
    if (pending.length === 0) return;
    const t = setInterval(async () => {
      const updated = await Promise.all(
        gens.map(async (g) => {
          if (TERMINAL.has(g.status)) return g;
          const res = await fetch(`/api/generations/${g.id}`);
          if (!res.ok) return g;
          return (await res.json()) as Gen;
        }),
      );
      setGens(updated);
    }, 3000);
    return () => clearInterval(t);
  }, [gens]);

  const upload = useCallback(
    async (file: File) => {
      setBusy(true);
      setNotice(null);
      try {
        const body = new FormData();
        body.append('photo', file);
        const res = await fetch('/api/upload', { method: 'POST', body });
        if (res.status === 402) {
          setNotice({ kind: 'err', text: 'Out of credits — buy more below.' });
          return;
        }
        if (!res.ok) {
          const j = await res.json().catch(() => ({}));
          setNotice({ kind: 'err', text: j.error ?? 'Upload failed.' });
          return;
        }
        const { id } = await res.json();
        setGens((g) => [{ id, status: 'queued' }, ...g]);
        setNotice({ kind: 'ok', text: 'Your poster is being drawn up, partner!' });
        await refreshBalance();
      } finally {
        setBusy(false);
      }
    },
    [refreshBalance],
  );

  const onDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDrag(false);
      const file = e.dataTransfer.files?.[0];
      if (file) void upload(file);
    },
    [upload],
  );

  const buyCredits = useCallback(async () => {
    setBusy(true);
    try {
      const res = await fetch('/api/checkout', { method: 'POST' });
      if (!res.ok) {
        setNotice({ kind: 'err', text: 'Could not start checkout.' });
        return;
      }
      const { url } = await res.json();
      window.location.href = url;
    } finally {
      setBusy(false);
    }
  }, []);

  return (
    <>
      {notice ? <div className={`notice ${notice.kind}`}>{notice.text}</div> : null}

      <div className="card">
        <div
          className={`dropzone ${drag ? 'drag' : ''}`}
          onClick={() => inputRef.current?.click()}
          onDragOver={(e) => {
            e.preventDefault();
            setDrag(true);
          }}
          onDragLeave={() => setDrag(false)}
          onDrop={onDrop}
        >
          {busy ? 'Working…' : 'Drag a photo here, or click to choose one (JPG/PNG/WebP, max 10MB)'}
        </div>
        <input
          ref={inputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp"
          style={{ display: 'none' }}
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) void upload(file);
          }}
        />
      </div>

      <div className="card balance">
        <div>
          <div className="sub">Need more posters?</div>
          <strong>Buy 10 credits for $1</strong>
        </div>
        <button className="btn" disabled={busy} onClick={() => void buyCredits()}>
          Buy 10 credits
        </button>
      </div>

      <h3>Recent posters</h3>
      {gens.length === 0 ? (
        <p className="sub">No posters yet — upload a photo to get started.</p>
      ) : (
        <div className="gen-grid">
          {gens.map((g) => (
            <div key={g.id} className="gen-tile">
              {g.posterUrl ? (
                <a href={g.posterUrl} target="_blank" rel="noreferrer">
                  <img src={g.posterUrl} alt="WANTED poster" />
                </a>
              ) : null}
              <div className={`status ${g.status === 'failed' ? 'failed' : ''}`}>
                {g.status === 'done'
                  ? 'Ready'
                  : g.status === 'failed'
                    ? `Failed${g.error ? `: ${g.error}` : ''}`
                    : g.status === 'processing'
                      ? 'Drawing…'
                      : 'Queued…'}
              </div>
            </div>
          ))}
        </div>
      )}
    </>
  );
}
