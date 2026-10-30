/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** UserMessage
*/

// Component from shadcn/ui: https://ui.shadcn.com/docs/components - icon from Lucide: https://lucide.dev/

import React, { useState } from 'react'
import { Pencil } from 'lucide-react'

import { Textarea } from '@/components/ui/textarea'
import type { Message } from '@/types/chat'

type UserMessageProps = {
  message: Message
  canEdit: boolean
  onEdit: (message: Message, text: string) => void
}

function UserMessage({ message, canEdit, onEdit }: UserMessageProps) {
  const [draft, setDraft] = useState<string | null>(null)
  const editable = canEdit && message.serverId !== undefined

  function save() {
    const text = (draft ?? '').trim()
    if (!editable || text === '' || text === message.content)
      return
    setDraft(null)
    onEdit(message, text)
  }

  function handleKeyDown(event: React.KeyboardEvent) {
    if (event.key === 'Escape')
      setDraft(null)
    if (event.key !== 'Enter' || event.shiftKey || event.nativeEvent.isComposing)
      return
    event.preventDefault()
    save()
  }

  if (draft !== null) {
    return (
      <div className="ml-auto w-full max-w-[80%] rounded-2xl border border-white/10 bg-white/10 p-2 backdrop-blur-md">
        <Textarea
          value={draft}
          autoFocus
          onChange={(event) => setDraft(event.target.value)}
          onKeyDown={handleKeyDown}
          aria-label="Edit your message"
          className="min-h-0 resize-none border-0 bg-transparent px-2 py-1 text-[0.95rem] leading-relaxed text-amber-50 shadow-none focus-visible:ring-0 md:text-[0.95rem] dark:bg-transparent"
        />
        <div className="mt-1.5 flex justify-end gap-1.5">
          <button
            type="button"
            onClick={() => setDraft(null)}
            className="rounded-full px-3 py-1 text-xs text-amber-100/60 transition-colors hover:text-amber-50"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={save}
            disabled={!editable || draft.trim() === '' || draft.trim() === message.content}
            className="rounded-full bg-amber-300 px-3 py-1 text-xs text-stone-950 transition-opacity disabled:opacity-40"
          >
            Send
          </button>
        </div>
      </div>
    )
  }
  return (
    <div className="group flex items-center justify-end gap-1.5">
      {editable && (
        <button
          type="button"
          aria-label="Edit this message"
          title="Edit this message"
          onClick={() => setDraft(message.content)}
          className="rounded-md p-1 text-amber-100/50 opacity-0 transition-opacity group-hover:opacity-100 hover:text-amber-50 focus-visible:opacity-100 pointer-coarse:opacity-100"
        >
          <Pencil className="size-3.5" />
        </button>
      )}
      <p className="max-w-[80%] rounded-2xl rounded-br-md border border-white/10 bg-white/10 px-4 py-2.5 text-[0.95rem] leading-relaxed whitespace-pre-wrap text-amber-50 backdrop-blur-md">
        {message.content}
      </p>
    </div>
  )
}

export default UserMessage
