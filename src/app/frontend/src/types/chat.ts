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
  role: Role
  content: string
  thinking?: string
  question?: Question
}

export type Profile = {
  key: string
  name: string
  role: string
}

export type ChatStatus = 'idle' | 'thinking' | 'streaming'

export type StreamEvent =
  | { type: 'thinking' | 'content'; text: string }
  | { type: 'done' }
  | { type: 'question'; text: string; options: string[] }
  | { type: 'spec'; text: string }
  | { type: 'error'; message: string }
