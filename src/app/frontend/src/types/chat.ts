/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** chat
*/

export type Role = 'user' | 'assistant'

export type Message = {
  id: string
  role: Role
  content: string
  thinking?: string
}

export type ChatStatus = 'idle' | 'thinking' | 'streaming'

export type StreamEvent =
  | { type: 'thinking' | 'content'; text: string }
  | { type: 'done' }
  | { type: 'error'; message: string }
