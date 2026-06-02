// lib/ses.ts — Transactional email via AWS SESv2: magic-link sign-in + "poster ready" notifications.
// Ch 27 notifications. Templates are inline + minimal; sender is SES_FROM_EMAIL.
import {
  SESv2Client,
  SendEmailCommand,
} from '@aws-sdk/client-sesv2';
import { env } from './env';

let client: SESv2Client | null = null;
function ses(): SESv2Client {
  if (!client) client = new SESv2Client({ region: env().AWS_REGION });
  return client;
}

async function send(to: string, subject: string, html: string, text: string): Promise<void> {
  await ses().send(
    new SendEmailCommand({
      FromEmailAddress: env().SES_FROM_EMAIL,
      Destination: { ToAddresses: [to] },
      Content: {
        Simple: {
          Subject: { Data: subject },
          Body: { Html: { Data: html }, Text: { Data: text } },
        },
      },
    }),
  );
}

/** Send a magic-link sign-in email. */
export async function sendMagicLink(to: string, link: string): Promise<void> {
  const subject = 'Your Wild West Wanted sign-in link';
  const text = `Howdy! Click to sign in: ${link}\n\nThis link expires in 15 minutes.`;
  const html = `<div style="font-family:Georgia,serif">
    <h2>Howdy, partner.</h2>
    <p>Click below to sign in to <strong>Wild West Wanted</strong>:</p>
    <p><a href="${link}" style="background:#7a4f1d;color:#fff;padding:10px 18px;text-decoration:none;border-radius:4px">Sign in</a></p>
    <p style="color:#666">This link expires in 15 minutes. If you didn't request it, ignore this email.</p>
  </div>`;
  await send(to, subject, html, text);
}

/** Notify the user their poster is ready, linking back to the app. */
export async function sendPosterReady(to: string, posterPageUrl: string): Promise<void> {
  const subject = 'Your WANTED poster is ready!';
  const text = `Your Old-West WANTED poster is ready. View it here: ${posterPageUrl}`;
  const html = `<div style="font-family:Georgia,serif">
    <h2>You're WANTED!</h2>
    <p>Your Old-West poster has finished generating.</p>
    <p><a href="${posterPageUrl}" style="background:#7a4f1d;color:#fff;padding:10px 18px;text-decoration:none;border-radius:4px">View your poster</a></p>
  </div>`;
  await send(to, subject, html, text);
}
