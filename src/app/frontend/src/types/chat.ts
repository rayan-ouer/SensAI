/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** chat
*/

export type Role = 'user' | 'assistant'

export type Question = {
  text: string
  options: string[]
}

export type Message = {
  id: string
  serverId?: string
  role: Role
  content: string
  thinking?: string
  question?: Question
  usage?: {
    promptTokens: number
    completionTokens: number
    totalTokens: number
  }
}

export type UploadedDocument = {
  id: string
  name: string
  status: 'indexing' | 'ready' | 'failed'
  detail?: string
}

export type Profile = {
  key: string
  name: string
  role: string
}

export type ChatStatus = 'idle' | 'thinking' | 'streaming'

export type StreamEvent =
  | { type: 'thinking' | 'content'; text: string }
  | { type: 'usage'; prompt_tokens: number; completion_tokens: number; total_tokens: number }
  | { type: 'done'; message_id: string }
  | { type: 'question'; text: string; options: string[] }
  | { type: 'spec'; text: string }
  | { type: 'error'; message: string }
