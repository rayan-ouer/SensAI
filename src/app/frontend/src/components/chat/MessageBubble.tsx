/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** MessageBubble
*/

import AssistantAvatar from '@/components/chat/AssistantAvatar'
import Reasoning from '@/components/chat/Reasoning'
import ThinkingIndicator from '@/components/chat/ThinkingIndicator'
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
  const thinking = message.content === ''
  const reasoning = message.thinking ?? ''
  return (
    <div className="flex items-start gap-3">
      <AssistantAvatar thinking={thinking} />
      <div className="max-w-[90%] pt-1">
        {reasoning !== '' && <Reasoning text={reasoning} active={thinking} />}
        {thinking ? (
          reasoning === '' && <ThinkingIndicator />
        ) : (
          <p className="animate-in text-[0.95rem] leading-relaxed whitespace-pre-wrap text-amber-50/90 duration-500 fade-in">
            {message.content}
          </p>
        )}
      </div>
    </div>
  )
}

export default MessageBubble
