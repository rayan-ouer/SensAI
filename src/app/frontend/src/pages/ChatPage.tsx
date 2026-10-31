/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** ChatPage
*/

// Icon from Lucide: https://lucide.dev/

import { useState } from 'react'
import { Activity, FileText, SquarePen } from 'lucide-react'

import Composer from '@/components/chat/Composer'
import DocumentList from '@/components/chat/DocumentList'
import DropZone from '@/components/chat/DropZone'
import EmptyState from '@/components/chat/EmptyState'
import MessageList from '@/components/chat/MessageList'
import ModelSelect from '@/components/chat/ModelSelect'
import ProfileSelect from '@/components/chat/ProfileSelect'
import SpecPanel from '@/components/spec/SpecPanel'
import MonitoringPage from '@/pages/MonitoringPage'
import { useChat } from '@/hooks/useChat'
import { useDocuments } from '@/hooks/useDocuments'
import { useModels } from '@/hooks/useModels'
import { useProfiles } from '@/hooks/useProfiles'
import { useSpec } from '@/hooks/useSpec'

const WIDE_SCREEN = '(min-width: 1024px)'

function ChatPage() {
  const spec = useSpec()
  const profiles = useProfiles()
  const models = useModels()
  const { messages, status, error, send, edit, reset, currentConversation } = useChat(spec, profiles.selected, models.selected)
  const documents = useDocuments(currentConversation)
  const [typing, setTyping] = useState(false)
  const [specOpen, setSpecOpen] = useState(() => window.matchMedia(WIDE_SCREEN).matches)
  const [monitoringOpen, setMonitoringOpen] = useState(false)

  function startNewConversation() {
    reset()
    documents.clear()
  }

  if (monitoringOpen)
    return <MonitoringPage onBack={() => setMonitoringOpen(false)} />

  return (
    <div className="flex h-dvh">
      <DropZone onDrop={documents.add}>
        <header className="mx-auto flex w-full max-w-2xl flex-wrap items-center justify-between gap-x-3 gap-y-2 px-4 py-4">
          <div className="flex min-w-0 items-center gap-3">
            <span className="shrink-0 text-sm font-medium tracking-tight text-amber-50">SensAI</span>
            <ProfileSelect
              profiles={profiles.profiles}
              selected={profiles.selected}
              disabled={status !== 'idle'}
              onSelect={profiles.select}
            />
          </div>
          <div className="ml-auto flex shrink-0 items-center gap-1">
            <ModelSelect
              models={models.models}
              selected={models.selected}
              disabled={status !== 'idle'}
              onSelect={models.select}
            />
            <button
              type="button"
              aria-label="Monitoring"
              title="Monitoring"
              onClick={() => setMonitoringOpen(true)}
              className="rounded-md p-1.5 text-amber-100/60 hover:bg-white/10 hover:text-amber-50"
            >
              <Activity className="size-4" />
            </button>
            {messages.length > 0 && (
              <button
                type="button"
                aria-label="New conversation"
                title="New conversation"
                onClick={startNewConversation}
                disabled={status !== 'idle'}
                className="rounded-md p-1.5 text-amber-100/60 hover:bg-white/10 hover:text-amber-50 disabled:opacity-40"
              >
                <SquarePen className="size-4" />
              </button>
            )}
            {!specOpen && (
              <button
                type="button"
                aria-label="Specification"
                title="Specification"
                onClick={() => setSpecOpen(true)}
                className="rounded-md p-1.5 text-amber-100/60 hover:bg-white/10 hover:text-amber-50"
              >
                <FileText className="size-4" />
              </button>
            )}
          </div>
        </header>
        <main className="flex min-h-0 flex-1 flex-col">
          {messages.length === 0 ? <EmptyState listening={typing} /> : <MessageList messages={messages} status={status} onAnswer={send} onEdit={edit} />}
        </main>
        <footer className="mx-auto w-full max-w-2xl px-4 pb-5">
          {error && <p role="alert" className="mb-2 px-2 text-sm text-red-300">{error}</p>}
          <DocumentList documents={documents.documents} onRemove={documents.remove} />
          <Composer onSend={send} onTyping={setTyping} onAttach={documents.add} disabled={status !== 'idle'} />
        </footer>
      </DropZone>
      {specOpen && <SpecPanel spec={spec.spec} updating={spec.updating} onClose={() => setSpecOpen(false)} />}
    </div>
  )
}

export default ChatPage
