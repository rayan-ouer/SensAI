/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** MessageBubble
*/

import AssistantAvatar from '@/components/chat/AssistantAvatar'
import QuestionCard from '@/components/chat/QuestionCard'
import Reasoning from '@/components/chat/Reasoning'
import ThinkingIndicator from '@/components/chat/ThinkingIndicator'
import type { Message } from '@/types/chat'

type MessageBubbleProps = {
  message: Message
  canAnswer: boolean
  onAnswer: (answer: string) => void
}

function MessageBubble({ message, canAnswer, onAnswer }: MessageBubbleProps) {
  if (message.role === 'user') {
    return (
      <div className="flex justify-end">
        <p className="max-w-[80%] rounded-2xl rounded-br-md border border-white/10 bg-white/10 px-4 py-2.5 text-[0.95rem] leading-relaxed whitespace-pre-wrap text-amber-50 backdrop-blur-md">
          {message.content}
        </p>
      </div>
    )
  }
  const thinking = message.content === '' && message.question === undefined
  const reasoning = message.thinking ?? ''
  return (
    <div className="flex items-start gap-3">
      <AssistantAvatar thinking={thinking} />
      <div className="max-w-[90%] pt-1">
        {reasoning !== '' && <Reasoning text={reasoning} active={thinking} />}
        {thinking && reasoning === '' && <ThinkingIndicator />}
        {message.content !== '' && (
          <p className="animate-in text-[0.95rem] leading-relaxed whitespace-pre-wrap text-amber-50/90 duration-500 fade-in">
            {message.content}
          </p>
        )}
        {message.question && <QuestionCard question={message.question} disabled={!canAnswer} onAnswer={onAnswer} />}
        {message.usage && (
          <p className="mt-2 text-xs text-amber-50/45">
            Tokens used: {message.usage.totalTokens.toLocaleString()} (input:{' '}
            {message.usage.promptTokens.toLocaleString()}, output:{' '}
            {message.usage.completionTokens.toLocaleString()})
          </p>
        )}
      </div>
    </div>
  )
}

export default MessageBubble
