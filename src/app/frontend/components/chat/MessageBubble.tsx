/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** MessageBubble
*/

import type { Message } from '@/types/chat'

type MessageBubbleProps = {
  message: Message
}

function MessageBubble({ message }: MessageBubbleProps) {
  if (message.role === 'user') {
    return (
      <div className="flex justify-end">
        <p className="max-w-[80%] rounded-2xl rounded-br-md border border-white/10 bg-white/10 px-4 py-2.5 text-[0.95rem] leading-relaxed whitespace-pre-wrap text-amber-50 backdrop-blur-md">
          {message.content}
        </p>
      </div>
    )
  }
  return (
    <p className="max-w-[90%] text-[0.95rem] leading-relaxed whitespace-pre-wrap text-amber-50/90">
      {message.content}
    </p>
  )
}

export default MessageBubble
