/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** AssistantAvatar
*/

// Orb from Thinking Orbs: https://rareformlabs.github.io/thinking-orbs/

import { useEffect, useState } from 'react'
import { ThinkingOrb } from 'thinking-orbs'

const FADE_MS = 500

const LAYER = 'absolute inset-0 transition-[scale,opacity,filter] duration-500 ease-out motion-reduce:transition-none'

type AssistantAvatarProps = {
  thinking: boolean
}

function AssistantAvatar({ thinking }: AssistantAvatarProps) {
  const [orbMounted, setOrbMounted] = useState(thinking)

  useEffect(() => {
    if (thinking)
      return
    const timer = setTimeout(() => setOrbMounted(false), FADE_MS)
    return () => clearTimeout(timer)
  }, [thinking])

  return (
    <div className="relative size-8 shrink-0">
      <img
        src="/avatar.svg"
        alt=""
        className={`${LAYER} size-8 ${thinking ? 'scale-75 opacity-0 blur-sm' : 'scale-100 opacity-100 blur-none'}`}
      />
      {orbMounted && (
        <div className={`${LAYER} animate-in fade-in zoom-in-75 duration-300 ${thinking ? 'scale-100 opacity-100' : 'scale-125 opacity-0 blur-sm'}`}>
          <ThinkingOrb state="working" size={32} theme="dark" color="#fcd34d" aria-label="The assistant is thinking" />
        </div>
      )}
    </div>
  )
}

export default AssistantAvatar
