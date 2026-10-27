/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** chatApi
*/

import type { StreamEvent } from '@/types/chat'

const API_URL = import.meta.env.VITE_API_URL ?? '/api'
const USER_ID = 'web'
const UNREACHABLE = 'Cannot reach the SensAI API. Is wu-api running?'
const GATEWAY_ERRORS = [502, 503, 504]

export class ConversationNotFoundError extends Error {}

async function failure(response: Response): Promise<Error> {
  if (GATEWAY_ERRORS.includes(response.status))
    return new Error(UNREACHABLE)
  const body = await response.json().catch(() => null)
  const detail = typeof body?.detail === 'string' ? body.detail : response.statusText
  if (response.status === 404)
    return new ConversationNotFoundError(detail)
  return new Error(`The API answered ${response.status}: ${detail}`)
}

async function post(path: string, payload: object): Promise<Response> {
  try {
    return await fetch(`${API_URL}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
  } catch {
    throw new Error(UNREACHABLE)
  }
}

export async function createConversation(): Promise<string> {
  const response = await post('/conversations/', { user_id: USER_ID })
  if (!response.ok)
    throw await failure(response)
  const body: { id: string } = await response.json()
  return body.id
}

async function* readLines(body: ReadableStream<Uint8Array>): AsyncGenerator<string> {
  const reader = body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  while (true) {
    const { value, done } = await reader.read()
    if (done)
      break
    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n')
    buffer = lines.pop() ?? ''
    yield* lines.filter((line) => line.trim() !== '')
  }
  if (buffer.trim() !== '')
    yield buffer
}

export async function* streamReply(conversationId: string, content: string): AsyncGenerator<StreamEvent> {
  const response = await post(`/conversations/${conversationId}/messages`, { content })
  if (!response.ok || response.body === null)
    throw await failure(response)
  for await (const line of readLines(response.body))
    yield JSON.parse(line) as StreamEvent
}
