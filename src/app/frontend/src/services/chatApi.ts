/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** chatApi
*/

import type { Message, Profile, StreamEvent } from '@/types/chat'

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

async function post(path: string, payload: object, method = 'POST'): Promise<Response> {
  try {
    return await fetch(`${API_URL}${path}`, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
  } catch {
    throw new Error(UNREACHABLE)
  }
}

export async function fetchSpec(): Promise<string> {
  const response = await fetch(`${API_URL}/spec`).catch(() => {
    throw new Error(UNREACHABLE)
  })
  if (!response.ok)
    throw await failure(response)
  const body: { content: string } = await response.json()
  return body.content
}

type StoredMessage = {
  id: string
  role: Message['role']
  content: string
  thinking: string | null
}

export async function fetchMessages(conversationId: string): Promise<Message[]> {
  const response = await fetch(`${API_URL}/conversations/${conversationId}/messages`).catch(() => {
    throw new Error(UNREACHABLE)
  })
  if (!response.ok)
    throw await failure(response)
  const body: { messages: StoredMessage[] } = await response.json()
  return body.messages.map((message) => ({
    id: crypto.randomUUID(),
    serverId: message.id,
    role: message.role,
    content: message.content,
    thinking: message.thinking ?? undefined,
  }))
}

export async function fetchProfiles(): Promise<{ profiles: Profile[]; default: string }> {
  const response = await fetch(`${API_URL}/profiles`).catch(() => {
    throw new Error(UNREACHABLE)
  })
  if (!response.ok)
    throw await failure(response)
  return response.json()
}

export async function fetchModels(): Promise<{ models: string[]; default: string }> {
  const response = await fetch(`${API_URL}/models`).catch(() => {
    throw new Error(UNREACHABLE)
  })
  if (!response.ok)
    throw await failure(response)
  return response.json()
}

export async function createConversation(): Promise<string> {
  const response = await post('/conversations/', { user_id: USER_ID })
  if (!response.ok)
    throw await failure(response)
  const body: { id: string } = await response.json()
  return body.id
}

export async function uploadDocument(conversationId: string, file: File): Promise<{ source: string; chunks: number }> {
  const form = new FormData()
  form.append('file', file)
  const response = await fetch(`${API_URL}/conversations/${conversationId}/documents`, {
    method: 'POST',
    body: form,
  }).catch(() => {
    throw new Error(UNREACHABLE)
  })
  if (!response.ok)
    throw await failure(response)
  return response.json()
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

export async function* streamReply(
  conversationId: string,
  content: string,
  profile: string | null,
  model: string | null,
  editedId: string | null,
): AsyncGenerator<StreamEvent> {
  const path = `/conversations/${conversationId}/messages`
  const payload = { content, profile, model }
  const response = await (editedId === null ? post(path, payload) : post(`${path}/${editedId}`, payload, 'PUT'))
  if (!response.ok || response.body === null)
    throw await failure(response)
  for await (const line of readLines(response.body))
    yield JSON.parse(line) as StreamEvent
}
