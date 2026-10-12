/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** ChatPage
*/

import Composer from '@/components/chat/Composer'
import EmptyState from '@/components/chat/EmptyState'
import MessageList from '@/components/chat/MessageList'
import { useChat } from '@/hooks/useChat'

function ChatPage() {
  const { messages, status, error, send } = useChat()

  return (
    <div className="flex h-dvh flex-col">
      <header className="mx-auto w-full max-w-2xl px-4 py-4">
        <span className="text-sm font-medium tracking-tight text-amber-50">SensAI</span>
      </header>
      <main className="flex min-h-0 flex-1 flex-col">
        {messages.length === 0 ? <EmptyState /> : <MessageList messages={messages} status={status} />}
      </main>
      <footer className="mx-auto w-full max-w-2xl px-4 pb-5">
        {error && <p role="alert" className="mb-2 px-2 text-sm text-red-300">{error}</p>}
        <Composer onSend={send} disabled={status !== 'idle'} />
      </footer>
    </div>
  )
}

export default ChatPage
