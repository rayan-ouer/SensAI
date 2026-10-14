/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** ThinkingIndicator
*/

// Text effect from React Bits: https://reactbits.dev/

import ShinyText from '@/components/effects/ShinyText'

function ThinkingIndicator() {
  return (
    <span role="status">
      <ShinyText text="Thinking" color="#a8a29e" shineColor="#fef3c7" speed={2} className="text-sm" />
    </span>
  )
}

export default ThinkingIndicator
