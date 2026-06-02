// lib/sqs.ts — Enqueue generation jobs onto the SQS standard queue for the worker to long-poll.
// Ch 26 async work / queues. The web app only enqueues; the worker owns Gemini + sharp compositing.
import { SQSClient, SendMessageCommand } from '@aws-sdk/client-sqs';
import { env } from './env';

let client: SQSClient | null = null;
function sqs(): SQSClient {
  if (!client) client = new SQSClient({ region: env().AWS_REGION });
  return client;
}

export interface GenerationJob {
  genId: string;
  userId: string;
  uploadKey: string;
}

/** Send a {genId,userId,uploadKey} job message. Called AFTER the credit-spend txn commits. */
export async function enqueueGeneration(job: GenerationJob): Promise<void> {
  await sqs().send(
    new SendMessageCommand({
      QueueUrl: env().SQS_QUEUE_URL,
      MessageBody: JSON.stringify({ kind: 'generation', ...job }),
    }),
  );
}
