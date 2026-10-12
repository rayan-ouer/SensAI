/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** ThinkingIndicator
*/

// Orb from Thinking Orbs: https://rareformlabs.github.io/thinking-orbs/ - text effect from React Bits: https://reactbits.dev/

import { ThinkingOrb } from 'thinking-orbs'

import ShinyText from '@/components/effects/ShinyText'

function ThinkingIndicator() {
  return (
    <div className="flex items-center gap-3" role="status">
      <ThinkingOrb state="working" size={32} theme="dark" color="#fcd34d" aria-label="The assistant is thinking" />
      <ShinyText text="Thinking" color="#a8a29e" shineColor="#fef3c7" speed={2} className="text-sm" />
    </div>
  )
}

export default ThinkingIndicator
