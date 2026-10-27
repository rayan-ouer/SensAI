/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** QuestionCard
*/

import type { Question } from '@/types/chat'

type QuestionCardProps = {
  question: Question
  disabled: boolean
  onAnswer: (answer: string) => void
}

function QuestionCard({ question, disabled, onAnswer }: QuestionCardProps) {
  return (
    <div className="mt-2 animate-in rounded-2xl border border-white/10 bg-black/30 p-3 duration-500 fade-in">
      <p className="text-[0.95rem] leading-relaxed text-amber-50/90">{question.text}</p>
      <div className="mt-2.5 flex flex-wrap gap-1.5">
        {question.options.map((option) => (
          <button
            key={option}
            type="button"
            disabled={disabled}
            onClick={() => onAnswer(option)}
            className="rounded-full border border-amber-300/40 px-3 py-1 text-xs text-amber-100 transition-colors hover:bg-amber-300 hover:text-stone-950 disabled:pointer-events-none disabled:opacity-40"
          >
            {option}
          </button>
        ))}
      </div>
      {!disabled && <p className="mt-2 text-xs text-amber-100/40">Or type another answer below.</p>}
    </div>
  )
}

export default QuestionCard
