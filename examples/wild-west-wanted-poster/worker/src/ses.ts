// ses.ts — Transactional email via AWS SES v2.
// Book chapter concept: "Notify out-of-band" — the worker emails the user when their poster is
// ready rather than holding an HTTP request open. Auth/magic-link email lives in the web app.

import { SESv2Client, SendEmailCommand } from '@aws-sdk/client-sesv2';

const region = process.env.AWS_REGION ?? 'us-west-2';
const fromEmail = process.env.SES_FROM_EMAIL ?? 'noreply@wildwestwanted.com';

/** Shared SES client. */
export const ses = new SESv2Client({ region });

/** Send a simple HTML + text email. Throws on SES failure so callers can decide to retry. */
export async function sendEmail(opts: {
  to: string;
  subject: string;
  html: string;
  text: string;
}): Promise<void> {
  await ses.send(
    new SendEmailCommand({
      FromEmailAddress: fromEmail,
      Destination: { ToAddresses: [opts.to] },
      Content: {
        Simple: {
          Subject: { Data: opts.subject, Charset: 'UTF-8' },
          Body: {
            Html: { Data: opts.html, Charset: 'UTF-8' },
            Text: { Data: opts.text, Charset: 'UTF-8' },
          },
        },
      },
    }),
  );
}

/** "Your wanted poster is ready" notification. */
export async function sendPosterReadyEmail(to: string, generationId: string): Promise<void> {
  const appUrl = process.env.APP_URL ?? 'https://wildwestwanted.com';
  const link = `${appUrl}/generations/${generationId}`;
  await sendEmail({
    to,
    subject: 'Yer WANTED poster is ready, partner',
    html: `<p>Reach for the sky &mdash; your Old-West wanted poster is ready.</p>
           <p><a href="${link}">View your poster</a></p>`,
    text: `Your Old-West wanted poster is ready. View it here: ${link}`,
  });
}
