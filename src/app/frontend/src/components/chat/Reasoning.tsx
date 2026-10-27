/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** Reasoning
*/

// Icon from Lucide: https://lucide.dev/

import { ChevronRight } from 'lucide-react'

import ThinkingIndicator from '@/components/chat/ThinkingIndicator'

type ReasoningProps = {
  text: string
  active: boolean
}

function Reasoning({ text, active }: ReasoningProps) {
  return (
    <details className="group mb-2 text-sm">
      <summary className="flex w-fit cursor-pointer list-none items-center gap-1 text-amber-100/50 select-none hover:text-amber-100/80 [&::-webkit-details-marker]:hidden">
        <ChevronRight className="size-3.5 transition-transform group-open:rotate-90" />
        {active ? <ThinkingIndicator /> : <span>Reasoning</span>}
      </summary>
      <p className="mt-2 max-h-60 overflow-y-auto border-l border-white/10 pl-3 text-[0.8rem] leading-relaxed whitespace-pre-wrap text-amber-100/50">
        {text}
      </p>
    </details>
  )
}

export default Reasoning
