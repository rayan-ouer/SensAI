/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** SpecPanel
*/

// Icon from Lucide: https://lucide.dev/ - text effect from React Bits: https://reactbits.dev/

import { X } from 'lucide-react'

import ShinyText from '@/components/effects/ShinyText'
import SpecContent from '@/components/spec/SpecContent'

type SpecPanelProps = {
  spec: string
  updating: boolean
  onClose: () => void
}

function SpecPanel({ spec, updating, onClose }: SpecPanelProps) {
  return (
    <aside className="fixed inset-y-0 right-0 z-20 flex w-full max-w-sm flex-col border-l border-white/10 bg-black/60 backdrop-blur-xl lg:static lg:z-auto lg:w-80 lg:bg-black/30">
      <div className="flex items-center justify-between px-4 py-4">
        <div className="flex items-baseline gap-2">
          <span className="text-sm font-medium tracking-tight text-amber-50">Specification</span>
          {updating && <ShinyText text="Updating" color="#a8a29e" shineColor="#fef3c7" speed={2} className="text-xs" />}
        </div>
        <button type="button" onClick={onClose} aria-label="Close the specification" className="rounded-md p-1 text-amber-100/50 hover:bg-white/10 hover:text-amber-50">
          <X className="size-4" />
        </button>
      </div>
      <div className="min-h-0 flex-1 overflow-y-auto px-4 pb-6 [scrollbar-color:rgb(255_255_255/0.15)_transparent] [scrollbar-width:thin]">
        {spec === '' ? (
          <p className="text-[0.8rem] text-amber-100/40">Describe your project in the chat: its specification will be written here.</p>
        ) : (
          <SpecContent text={spec} />
        )}
      </div>
    </aside>
  )
}

export default SpecPanel
