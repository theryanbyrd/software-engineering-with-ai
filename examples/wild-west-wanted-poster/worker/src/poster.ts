// poster.ts — Composite the final "WANTED" poster with sharp.
// Book chapter concept: "Deterministic post-processing in-process" — the creative/expensive step
// is Gemini; the frame (parchment, WANTED header, reward line, name) is cheap, deterministic
// compositing we own end-to-end. Output is PNG bytes ready to store in S3.

import sharp from 'sharp';

const WIDTH = 1024;
const HEIGHT = 1536;
const PORTRAIT_BOX = 720; // square portrait window inside the frame

/** Pick a believably absurd Old-West bounty. */
export function randomReward(): number {
  // $500 .. $50,000 rounded to a "poster-friendly" round number.
  const tiers = [500, 1000, 2500, 5000, 10000, 25000, 50000];
  return tiers[Math.floor(Math.random() * tiers.length)];
}

/** Escape text for safe inclusion in the SVG overlay. */
function xmlEscape(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

/** Build the parchment background as a sepia gradient with a torn-edge feel. */
function parchmentSvg(): Buffer {
  return Buffer.from(`
    <svg width="${WIDTH}" height="${HEIGHT}" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <radialGradient id="paper" cx="50%" cy="40%" r="80%">
          <stop offset="0%" stop-color="#f3e3c0"/>
          <stop offset="70%" stop-color="#e3cda0"/>
          <stop offset="100%" stop-color="#c9ad7a"/>
        </radialGradient>
      </defs>
      <rect width="${WIDTH}" height="${HEIGHT}" fill="url(#paper)"/>
      <rect x="24" y="24" width="${WIDTH - 48}" height="${HEIGHT - 48}"
            fill="none" stroke="#5b3a1a" stroke-width="8"/>
      <rect x="44" y="44" width="${WIDTH - 88}" height="${HEIGHT - 88}"
            fill="none" stroke="#5b3a1a" stroke-width="2"/>
    </svg>`);
}

/** Build the text overlay (header, sub-header, reward, name). */
function textSvg(name: string, reward: number): Buffer {
  const safeName = xmlEscape(name.trim() || 'The Stranger').toUpperCase();
  const rewardStr = `$${reward.toLocaleString('en-US')}`;
  const portraitTop = 300;
  const portraitBottom = portraitTop + PORTRAIT_BOX;
  return Buffer.from(`
    <svg width="${WIDTH}" height="${HEIGHT}" xmlns="http://www.w3.org/2000/svg">
      <style>
        .head { font-family: 'Georgia','Times New Roman',serif; font-weight: 900; fill: #3a2410; }
        .sub  { font-family: 'Georgia','Times New Roman',serif; font-weight: 700; fill: #4a2f14; }
        .name { font-family: 'Georgia','Times New Roman',serif; font-weight: 800; fill: #2f1d0c; }
      </style>
      <text x="${WIDTH / 2}" y="170" text-anchor="middle" class="head"
            font-size="150" letter-spacing="14">WANTED</text>
      <text x="${WIDTH / 2}" y="250" text-anchor="middle" class="sub"
            font-size="58" letter-spacing="10">DEAD OR ALIVE</text>
      <text x="${WIDTH / 2}" y="${portraitBottom + 110}" text-anchor="middle" class="name"
            font-size="70" letter-spacing="6">${safeName}</text>
      <text x="${WIDTH / 2}" y="${portraitBottom + 210}" text-anchor="middle" class="sub"
            font-size="46" letter-spacing="6">REWARD</text>
      <text x="${WIDTH / 2}" y="${portraitBottom + 280}" text-anchor="middle" class="head"
            font-size="96" letter-spacing="4">${rewardStr}</text>
    </svg>`);
}

export interface PosterInput {
  /** Sepia portrait bytes from Gemini. */
  portrait: Buffer;
  /** Display name for the wanted person. */
  name: string;
  /** Reward amount in whole dollars (use randomReward() if not supplied). */
  reward?: number;
}

/**
 * Composite parchment + framed portrait + text into the final poster.
 * Returns PNG bytes.
 */
export async function composePoster(input: PosterInput): Promise<Buffer> {
  const reward = input.reward ?? randomReward();
  const portraitTop = 300;
  const portraitLeft = Math.round((WIDTH - PORTRAIT_BOX) / 2);

  // Sepia-tone + fit the portrait into the square window, then add a dark frame border.
  const framedPortrait = await sharp(input.portrait)
    .resize(PORTRAIT_BOX, PORTRAIT_BOX, { fit: 'cover', position: 'attention' })
    .modulate({ saturation: 0.6 })
    .tint({ r: 190, g: 150, b: 100 }) // warm sepia
    .extend({ top: 10, bottom: 10, left: 10, right: 10, background: '#3a2410' })
    .png()
    .toBuffer();

  const poster = await sharp(parchmentSvg())
    .composite([
      { input: framedPortrait, top: portraitTop - 10, left: portraitLeft - 10 },
      { input: textSvg(input.name, reward), top: 0, left: 0 },
    ])
    .png()
    .toBuffer();

  return poster;
}
