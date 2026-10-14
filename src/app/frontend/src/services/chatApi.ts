/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** chatApi
*/

import type { Message } from '@/types/chat'

const THINKING_DELAY_MS = 1400
const TOKEN_DELAY_MS = 35

function wait(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

// Mock of the backend: yields a reply piece by piece, like the real stream will.
// Replace the body with a call to the API once it exists; the page only relies on this signature.
export async function* streamReply(messages: Message[]): AsyncGenerator<string> {
  const lastMessage = messages[messages.length - 1]
  const reply = `The API is not connected yet, so this is a placeholder reply. You said: "${lastMessage.content}"`

  await wait(THINKING_DELAY_MS)
  for (const word of reply.split(' ')) {
    await wait(TOKEN_DELAY_MS)
    yield `${word} `
  }
}
