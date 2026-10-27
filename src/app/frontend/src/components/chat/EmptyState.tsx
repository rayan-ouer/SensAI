/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** EmptyState
*/

import LogoParticles from '@/components/chat/LogoParticles'

type EmptyStateProps = {
  listening: boolean
}

function EmptyState({ listening }: EmptyStateProps) {
  return (
    <div className="flex flex-1 flex-col items-center justify-center gap-5 text-center">
      <LogoParticles active={listening} />
      <div className="space-y-1.5">
        <h1 className="text-2xl font-medium tracking-tight text-amber-50">What are we building today?</h1>
        <p className="text-sm text-amber-100/60">Describe your project and SensAI keeps its specification up to date.</p>
      </div>
    </div>
  )
}

export default EmptyState
