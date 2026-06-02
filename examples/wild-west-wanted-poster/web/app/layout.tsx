// app/layout.tsx — Root layout + western letterhead. Server component. Ch 13 worked-example shell.
import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Wild West Wanted Poster',
  description: 'Upload a photo, get an AI-generated Old-West WANTED poster of yourself.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="container">
          <header className="brand">
            <div className="sub">— By order of the territory —</div>
            <h1>Wanted</h1>
            <div className="sub">Wild West Wanted Poster</div>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
