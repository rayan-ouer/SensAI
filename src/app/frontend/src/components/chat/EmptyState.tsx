/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** EmptyState
*/

// Orb from Thinking Orbs: https://rareformlabs.github.io/thinking-orbs/

import { ThinkingOrb } from 'thinking-orbs'

function EmptyState() {
  return (
    <div className="flex flex-1 flex-col items-center justify-center gap-5 text-center">
      <ThinkingOrb state="breathing" size={64} theme="dark" color="#fcd34d" aria-label="SensAI is ready" />
      <div className="space-y-1.5">
        <h1 className="text-2xl font-medium tracking-tight text-amber-50">What are we building today?</h1>
        <p className="text-sm text-amber-100/60">Describe your project and SensAI keeps its specification up to date.</p>
      </div>
    </div>
  )
}

export default EmptyState
