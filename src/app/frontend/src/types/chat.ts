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
}

export type ChatStatus = 'idle' | 'thinking' | 'streaming'
