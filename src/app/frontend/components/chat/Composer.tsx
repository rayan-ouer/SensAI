/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** Composer
*/

// Components from shadcn/ui: https://ui.shadcn.com/docs/components - icon from Lucide: https://lucide.dev/

import React, { useState } from 'react'
import { ArrowUp } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'

type ComposerProps = {
  onSend: (text: string) => void
  disabled: boolean
}

function Composer({ onSend, disabled }: ComposerProps) {
  const [text, setText] = useState('')
  const canSend = !disabled && text.trim() !== ''

  function submit() {
    if (!canSend)
      return
    onSend(text.trim())
    setText('')
  }

  function handleSubmit(event: React.SubmitEvent) {
    event.preventDefault()
    submit()
  }

  function handleKeyDown(event: React.KeyboardEvent) {
    if (event.key !== 'Enter' || event.shiftKey || event.nativeEvent.isComposing)
      return
    event.preventDefault()
    submit()
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="flex items-end gap-2 rounded-3xl border border-white/10 bg-black/40 p-2 pl-4 shadow-2xl shadow-black/40 backdrop-blur-xl focus-within:border-white/20"
    >
      <Textarea
        value={text}
        onChange={(event) => setText(event.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Message SensAI..."
        aria-label="Message"
        rows={1}
        autoFocus
        className="max-h-48 min-h-9 resize-none border-0 bg-transparent px-0 py-1.5 text-[0.95rem] text-amber-50 shadow-none placeholder:text-amber-100/40 focus-visible:border-0 focus-visible:ring-0 md:text-[0.95rem] dark:bg-transparent"
      />
      <Button
        type="submit"
        size="icon-lg"
        disabled={!canSend}
        aria-label="Send message"
        className="rounded-full bg-amber-300 text-stone-950 hover:bg-amber-200 disabled:bg-white/10 disabled:text-amber-100/40 disabled:opacity-100"
      >
        <ArrowUp />
      </Button>
    </form>
  )
}

export default Composer
