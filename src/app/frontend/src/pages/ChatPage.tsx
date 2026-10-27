/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** ChatPage
*/

// Icon from Lucide: https://lucide.dev/

import { useState } from 'react'
import { FileText, SquarePen } from 'lucide-react'

import Composer from '@/components/chat/Composer'
import EmptyState from '@/components/chat/EmptyState'
import MessageList from '@/components/chat/MessageList'
import ProfileSelect from '@/components/chat/ProfileSelect'
import SpecPanel from '@/components/spec/SpecPanel'
import { useChat } from '@/hooks/useChat'
import { useProfiles } from '@/hooks/useProfiles'
import { useSpec } from '@/hooks/useSpec'

const WIDE_SCREEN = '(min-width: 1024px)'

function ChatPage() {
  const spec = useSpec()
  const profiles = useProfiles()
  const { messages, status, error, send, reset } = useChat(spec, profiles.selected)
  const [typing, setTyping] = useState(false)
  const [specOpen, setSpecOpen] = useState(() => window.matchMedia(WIDE_SCREEN).matches)

  return (
    <div className="flex h-dvh">
      <div className="flex min-w-0 flex-1 flex-col">
        <header className="mx-auto flex w-full max-w-2xl items-center justify-between px-4 py-4">
          <div className="flex items-center gap-3">
            <span className="text-sm font-medium tracking-tight text-amber-50">SensAI</span>
            <ProfileSelect
              profiles={profiles.profiles}
              selected={profiles.selected}
              disabled={status !== 'idle'}
              onSelect={profiles.select}
            />
          </div>
          <div className="flex items-center gap-1">
            {messages.length > 0 && (
              <button
                type="button"
                onClick={reset}
                disabled={status !== 'idle'}
                className="flex items-center gap-1.5 rounded-md px-2 py-1 text-xs text-amber-100/60 hover:bg-white/10 hover:text-amber-50 disabled:opacity-40"
              >
                <SquarePen className="size-3.5" />
                New conversation
              </button>
            )}
            {!specOpen && (
              <button
                type="button"
                onClick={() => setSpecOpen(true)}
                className="flex items-center gap-1.5 rounded-md px-2 py-1 text-xs text-amber-100/60 hover:bg-white/10 hover:text-amber-50"
              >
                <FileText className="size-3.5" />
                Specification
              </button>
            )}
          </div>
        </header>
        <main className="flex min-h-0 flex-1 flex-col">
          {messages.length === 0 ? <EmptyState listening={typing} /> : <MessageList messages={messages} status={status} />}
        </main>
        <footer className="mx-auto w-full max-w-2xl px-4 pb-5">
          {error && <p role="alert" className="mb-2 px-2 text-sm text-red-300">{error}</p>}
          <Composer onSend={send} onTyping={setTyping} disabled={status !== 'idle'} />
        </footer>
      </div>
      {specOpen && <SpecPanel spec={spec.spec} updating={spec.updating} onClose={() => setSpecOpen(false)} />}
    </div>
  )
}

export default ChatPage
