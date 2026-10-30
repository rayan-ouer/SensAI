/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** ModelSelect
*/

// Icon from Lucide: https://lucide.dev/

import { ChevronDown } from 'lucide-react'
import { Select } from 'radix-ui'

type ModelSelectProps = {
  models: string[]
  selected: string | null
  disabled: boolean
  onSelect: (model: string) => void
}

function ModelSelect({ models, selected, disabled, onSelect }: ModelSelectProps) {
  if (models.length < 2)
    return null
  return (
    <Select.Root value={selected ?? ''} disabled={disabled} onValueChange={onSelect}>
      <Select.Trigger
        aria-label="Model"
        className="flex max-w-40 items-center gap-1 rounded-full border border-white/10 bg-black/30 py-1 pr-1.5 pl-2.5 text-xs text-amber-100/60 outline-none transition-colors hover:text-amber-50 focus-visible:border-amber-300/40 disabled:cursor-not-allowed disabled:opacity-40"
      >
        <span className="truncate">
          <Select.Value />
        </span>
        <Select.Icon>
          <ChevronDown className="size-3.5 shrink-0" />
        </Select.Icon>
      </Select.Trigger>
      <Select.Portal>
        <Select.Content
          position="popper"
          align="end"
          sideOffset={6}
          className="z-50 animate-in overflow-hidden rounded-xl border border-white/10 bg-stone-950 shadow-lg duration-150 fade-in"
        >
          <Select.Viewport className="p-1">
            {models.map((model) => (
              <Select.Item
                key={model}
                value={model}
                className="cursor-pointer rounded-lg px-2.5 py-1.5 text-xs text-amber-100/70 outline-none transition-colors data-[state=checked]:bg-amber-300 data-[state=checked]:text-stone-950 data-[state=unchecked]:data-highlighted:bg-white/10 data-[state=unchecked]:data-highlighted:text-amber-50"
              >
                <Select.ItemText>{model}</Select.ItemText>
              </Select.Item>
            ))}
          </Select.Viewport>
        </Select.Content>
      </Select.Portal>
    </Select.Root>
  )
}

export default ModelSelect
