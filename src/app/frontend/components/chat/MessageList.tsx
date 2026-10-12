/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** MessageList
*/

import { useEffect, useRef } from 'react'

import MessageBubble from '@/components/chat/MessageBubble'
import ThinkingIndicator from '@/components/chat/ThinkingIndicator'
import type { ChatStatus, Message } from '@/types/chat'

type MessageListProps = {
  messages: Message[]
  status: ChatStatus
}

function MessageList({ messages, status }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ block: 'end' })
  }, [messages, status])

  return (
    <div className="flex-1 overflow-y-auto [mask-image:linear-gradient(to_bottom,transparent,black_1.5rem,black_calc(100%-1.5rem),transparent)] [scrollbar-color:rgb(255_255_255/0.15)_transparent] [scrollbar-gutter:stable_both-edges] [scrollbar-width:thin]">
      <div className="mx-auto flex w-full max-w-2xl flex-col gap-5 px-4 py-6" aria-live="polite">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        {status === 'thinking' && <ThinkingIndicator />}
        <div ref={bottomRef} />
      </div>
    </div>
  )
}

export default MessageList
