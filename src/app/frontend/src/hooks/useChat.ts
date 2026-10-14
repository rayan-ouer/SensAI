/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** useChat
*/

import { useState } from 'react'

import { streamReply } from '@/services/chatApi'
import type { ChatStatus, Message } from '@/types/chat'

function appendToMessage(messages: Message[], id: string, chunk: string): Message[] {
  return messages.map((message) =>
    message.id === id ? { ...message, content: message.content + chunk } : message
  )
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [status, setStatus] = useState<ChatStatus>('idle')
  const [error, setError] = useState<string | null>(null)

  async function receiveReply(history: Message[]) {
    const replyId = crypto.randomUUID()
    let started = false

    for await (const chunk of streamReply(history)) {
      if (!started) {
        started = true
        setStatus('streaming')
        setMessages((current) => [...current, { id: replyId, role: 'assistant', content: chunk }])
      } else {
        setMessages((current) => appendToMessage(current, replyId, chunk))
      }
    }
  }

  async function send(text: string) {
    if (status !== 'idle')
      return
    const userMessage: Message = { id: crypto.randomUUID(), role: 'user', content: text }
    const history = [...messages, userMessage]

    setMessages(history)
    setError(null)
    setStatus('thinking')
    try {
      await receiveReply(history)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'The assistant could not reply.')
    } finally {
      setStatus('idle')
    }
  }

  return { messages, status, error, send }
}
