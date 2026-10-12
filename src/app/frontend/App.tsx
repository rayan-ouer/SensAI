/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** App
*/

import { lazy, Suspense } from 'react'

import AuraBackground from '@/components/layout/AuraBackground'
import PageLoader from '@/components/layout/PageLoader'

const ChatPage = lazy(() => import('@/pages/ChatPage'))

function App() {
  return (
    <>
      <AuraBackground />
      <Suspense fallback={<PageLoader />}>
        <ChatPage />
      </Suspense>
    </>
  )
}

export default App
