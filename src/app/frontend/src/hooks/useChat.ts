/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** useChat
*/

import { useEffect, useRef, useState } from 'react'

import { ConversationNotFoundError, createConversation, fetchMessages, streamReply } from '@/services/chatApi'
import type { SpecState } from '@/hooks/useSpec'
import type { ChatStatus, Message, Question } from '@/types/chat'

type SpecUpdates = Pick<SpecState, 'startUpdate' | 'receive' | 'stopUpdate'>

const STORAGE_KEY = 'sensai.conversation'

function readStoredId(): string | null {
  try {
    return localStorage.getItem(STORAGE_KEY)
  } catch {
    return null
  }
}

function storeId(id: string | null) {
  try {
    if (id === null)
      localStorage.removeItem(STORAGE_KEY)
    else
      localStorage.setItem(STORAGE_KEY, id)
  } catch {
    return
  }
}

function appendToMessage(messages: Message[], id: string, field: 'content' | 'thinking', chunk: string): Message[] {
  return messages.map((message) =>
    message.id === id ? { ...message, [field]: (message[field] ?? '') + chunk } : message
  )
}

function attachQuestion(messages: Message[], id: string, question: Question): Message[] {
  return messages.map((message) => (message.id === id ? { ...message, question } : message))
}

export function useChat(spec: SpecUpdates, profile: string | null, model: string | null) {
  const [messages, setMessages] = useState<Message[]>([])
  const [status, setStatus] = useState<ChatStatus>('idle')
  const [error, setError] = useState<string | null>(null)
  const conversationId = useRef<string | null>(null)
  const activeReply = useRef<string | null>(null)

  useEffect(() => {
    const storedId = readStoredId()
    if (storedId === null)
      return
    fetchMessages(storedId)
      .then((stored) => {
        conversationId.current = storedId
        setMessages(stored)
      })
      .catch(() => storeId(null))
  }, [])

  async function currentConversation(): Promise<string> {
    if (conversationId.current === null) {
      conversationId.current = await createConversation()
      storeId(conversationId.current)
    }
    return conversationId.current
  }

  function reset() {
    if (status !== 'idle')
      return
    conversationId.current = null
    storeId(null)
    setMessages([])
    setError(null)
  }

  async function receiveReply(text: string, replyId: string) {
    for await (const event of streamReply(await currentConversation(), text, profile, model)) {
      if (event.type === 'error')
        throw new Error(event.message)
      if (event.type === 'thinking')
        setMessages((current) => appendToMessage(current, replyId, 'thinking', event.text))
      if (event.type === 'content') {
        setStatus('streaming')
        setMessages((current) => appendToMessage(current, replyId, 'content', event.text))
      }
      if (event.type === 'question')
        setMessages((current) => attachQuestion(current, replyId, { text: event.text, options: event.options }))
      if (event.type === 'done') {
        setStatus('idle')
        spec.startUpdate()
      }
      if (event.type === 'spec')
        spec.receive(event.text)
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
    setMessages((current) => current.filter((message) => message.id !== replyId || message.content !== '' || message.question !== undefined))
  }

  async function send(text: string) {
    if (status !== 'idle')
      return
    const userMessage: Message = { id: crypto.randomUUID(), role: 'user', content: text }
    const reply: Message = { id: crypto.randomUUID(), role: 'assistant', content: '' }

    activeReply.current = reply.id
    setMessages((current) => [...current, userMessage, reply])
    setError(null)
    setStatus('thinking')
    try {
      await receiveReplyOrRetry(text, reply.id)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'The assistant could not reply.')
    } finally {
      dropEmptyReply(reply.id)
      if (activeReply.current === reply.id) {
        setStatus('idle')
        spec.stopUpdate()
      }
    }
  }

  return { messages, status, error, send, reset }
}
