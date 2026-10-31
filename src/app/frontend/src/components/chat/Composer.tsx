/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** Composer
*/

// Components from shadcn/ui: https://ui.shadcn.com/docs/components - icon from Lucide: https://lucide.dev/

import React, { useRef, useState } from 'react'
import { ArrowUp, Paperclip } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { SUPPORTED_EXTENSIONS } from '@/hooks/useDocuments'

type ComposerProps = {
  onSend: (text: string) => void
  onTyping?: (typing: boolean) => void
  onAttach: (files: File[]) => void
  disabled: boolean
}

function Composer({ onSend, onTyping, onAttach, disabled }: ComposerProps) {
  const [text, setText] = useState('')
  const fileInput = useRef<HTMLInputElement>(null)
  const canSend = !disabled && text.trim() !== ''

  function submit() {
    if (!canSend)
      return
    onSend(text.trim())
    changeText('')
  }

  function changeText(value: string) {
    setText(value)
    onTyping?.(value.trim() !== '')
  }

  function handleSubmit(event: React.SubmitEvent) {
    event.preventDefault()
    submit()
  }

  function handleFiles(event: React.ChangeEvent<HTMLInputElement>) {
    onAttach([...(event.target.files ?? [])])
    event.target.value = ''
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
      className="flex items-end gap-1.5 rounded-3xl border border-white/10 bg-black/40 p-2 shadow-2xl shadow-black/40 backdrop-blur-xl focus-within:border-white/20"
    >
      <input
        ref={fileInput}
        type="file"
        multiple
        hidden
        accept={SUPPORTED_EXTENSIONS.join(',')}
        onChange={handleFiles}
      />
      <Button
        type="button"
        variant="ghost"
        size="icon-lg"
        aria-label="Add a document"
        title="Add a document"
        onClick={() => fileInput.current?.click()}
        className="rounded-full text-amber-100/60 hover:bg-white/10 hover:text-amber-50"
      >
        <Paperclip />
      </Button>
      <Textarea
        value={text}
        onChange={(event) => changeText(event.target.value)}
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
