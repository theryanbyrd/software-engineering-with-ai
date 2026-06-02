// gemini.ts — Transform an uploaded portrait into an Old-West "wanted poster" portrait via Gemini.
// Book chapter concept: "Calling a paid AI model behind the queue" — the worker (not the web
// request) spends the slow/expensive Gemini call, keeping the user-facing API fast and cheap.
// Model: gemini-2.5-flash-image via @google/genai.

import { GoogleGenAI } from '@google/genai';

const MODEL = 'gemini-2.5-flash-image';

const apiKey = process.env.GEMINI_API_KEY;
if (!apiKey) {
  throw new Error('GEMINI_API_KEY is required');
}

const ai = new GoogleGenAI({ apiKey });

/**
 * The image-to-image prompt. We keep it explicit so output is consistent and reviewable:
 * sepia, vintage, head-and-shoulders, neutral background that composites cleanly onto parchment.
 */
const POSTER_PROMPT = [
  'Transform the supplied portrait photo into a vintage 1880s American Old-West "wanted poster"',
  'portrait of the SAME person. Render it as a hand-drawn sepia-toned engraving / aged photograph:',
  'warm brown sepia tones, soft grain, slightly faded edges, period-accurate clothing',
  '(rugged frontier shirt, vest, or duster; optional cowboy hat). Keep the face clearly recognizable.',
  'Head-and-shoulders framing, centered, looking toward camera, plain aged-paper background',
  'with no text. Photorealistic-but-antique look suitable for printing on a parchment poster.',
].join(' ');

export interface GeminiResult {
  /** Raw image bytes returned by the model. */
  bytes: Buffer;
  /** MIME type reported by the model (e.g. image/png). */
  mimeType: string;
}

/**
 * Send the user's uploaded portrait to Gemini and return the generated sepia portrait bytes.
 * @param inputImage  the original uploaded image bytes
 * @param inputMime   the original image MIME type (default image/jpeg)
 */
export async function generateWantedPortrait(
  inputImage: Buffer,
  inputMime = 'image/jpeg',
): Promise<GeminiResult> {
  const response = await ai.models.generateContent({
    model: MODEL,
    contents: [
      {
        role: 'user',
        parts: [
          { text: POSTER_PROMPT },
          {
            inlineData: {
              mimeType: inputMime,
              data: inputImage.toString('base64'),
            },
          },
        ],
      },
    ],
  });

  // Walk the response parts and pick the first inline image payload.
  const parts = response.candidates?.[0]?.content?.parts ?? [];
  for (const part of parts) {
    const inline = part.inlineData;
    if (inline?.data) {
      return {
        bytes: Buffer.from(inline.data, 'base64'),
        mimeType: inline.mimeType ?? 'image/png',
      };
    }
  }

  throw new Error('Gemini returned no image data for the wanted-poster portrait');
}
