/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** MessageList
*/

import { useEffect, useRef } from 'react'

import MessageBubble from '@/components/chat/MessageBubble'
import type { ChatStatus, Message } from '@/types/chat'

type MessageListProps = {
  messages: Message[]
  status: ChatStatus
  onAnswer: (answer: string) => void
  onEdit: (message: Message, text: string) => void
}

function MessageList({ messages, status, onAnswer, onEdit }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ block: 'end' })
  }, [messages, status])

  return (
    <div className="flex-1 overflow-y-auto [mask-image:linear-gradient(to_bottom,transparent,black_1.5rem,black_calc(100%-1.5rem),transparent)] [scrollbar-color:rgb(255_255_255/0.15)_transparent] [scrollbar-gutter:stable_both-edges] [scrollbar-width:thin]">
      <div className="mx-auto flex w-full max-w-2xl flex-col gap-5 px-4 py-6" aria-live="polite">
        {messages.map((message, index) => (
          <MessageBubble
            key={message.id}
            message={message}
            canAnswer={status === 'idle' && index === messages.length - 1}
            canEdit={status === 'idle'}
            onAnswer={onAnswer}
            onEdit={onEdit}
          />
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  )
}

export default MessageList
