import type { ThoughtResponse } from '../types';

interface ThoughtRequest {
  prompt: string;
  model: string;
}

const MAX_RETRIES = 3;
const RETRY_DELAY = 1000; // 1 second

async function sleep(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * No need for this here
 */
async function retryRequest(fn: () => Promise<any>, retries = MAX_RETRIES): Promise<any> {
  try {
    return await fn();
  } catch (error) {
    if (retries > 0) {
      await sleep(RETRY_DELAY);
      return retryRequest(fn, retries - 1);
    }
    throw error;
  }
}

export async function runThoughtPrompt(request: ThoughtRequest): Promise<ThoughtResponse> {
  const makeRequest = async () => {
    const response = await fetch('/thought-prompt', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return {
      thoughts: data.thoughts,
      response: data.response,
      error: data.error
    } as ThoughtResponse;
  };

  try {
    return await makeRequest();
  } catch (error) {
    console.error('Error running thought prompt:', error);
    return {
      thoughts: '',
      response: '',
      error: (error as Error).message
    };
  }
}
