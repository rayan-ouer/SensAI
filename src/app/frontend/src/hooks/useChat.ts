/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** useChat
*/

import { useRef, useState } from 'react'

import { ConversationNotFoundError, createConversation, streamReply } from '@/services/chatApi'
import type { ChatStatus, Message } from '@/types/chat'

function appendToMessage(messages: Message[], id: string, field: 'content' | 'thinking', chunk: string): Message[] {
  return messages.map((message) =>
    message.id === id ? { ...message, [field]: (message[field] ?? '') + chunk } : message
  )
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [status, setStatus] = useState<ChatStatus>('idle')
  const [error, setError] = useState<string | null>(null)
  const conversationId = useRef<string | null>(null)

  async function currentConversation(): Promise<string> {
    conversationId.current ??= await createConversation()
    return conversationId.current
  }

  async function receiveReply(text: string, replyId: string) {
    for await (const event of streamReply(await currentConversation(), text)) {
      if (event.type === 'error')
        throw new Error(event.message)
      if (event.type === 'thinking')
        setMessages((current) => appendToMessage(current, replyId, 'thinking', event.text))
      if (event.type === 'content') {
        setStatus('streaming')
        setMessages((current) => appendToMessage(current, replyId, 'content', event.text))
      }
    }
  }

  async function receiveReplyOrRetry(text: string, replyId: string) {
    try {
      await receiveReply(text, replyId)
    } catch (e) {
      if (!(e instanceof ConversationNotFoundError))
        throw e
      conversationId.current = null
      await receiveReply(text, replyId)
    }
  }

  function dropEmptyReply(replyId: string) {
    setMessages((current) => current.filter((message) => message.id !== replyId || message.content !== ''))
  }

  async function send(text: string) {
    if (status !== 'idle')
      return
    const userMessage: Message = { id: crypto.randomUUID(), role: 'user', content: text }
    const reply: Message = { id: crypto.randomUUID(), role: 'assistant', content: '' }

    setMessages((current) => [...current, userMessage, reply])
    setError(null)
    setStatus('thinking')
    try {
      await receiveReplyOrRetry(text, reply.id)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'The assistant could not reply.')
    } finally {
      dropEmptyReply(reply.id)
      setStatus('idle')
    }
  }

  return { messages, status, error, send }
}
