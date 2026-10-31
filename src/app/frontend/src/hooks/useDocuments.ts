/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** useDocuments
*/

import { useState } from 'react'

import { uploadDocument } from '@/services/chatApi'
import type { UploadedDocument } from '@/types/chat'

export const SUPPORTED_EXTENSIONS = ['.pdf', '.md', '.markdown', '.txt', '.csv']

function isSupported(file: File): boolean {
  const name = file.name.toLowerCase()
  return SUPPORTED_EXTENSIONS.some((extension) => name.endsWith(extension))
}

export function useDocuments(conversation: () => Promise<string>) {
  const [documents, setDocuments] = useState<UploadedDocument[]>([])

  function change(id: string, update: Partial<UploadedDocument>) {
    setDocuments((current) => current.map((document) => (document.id === id ? { ...document, ...update } : document)))
  }

  async function upload(file: File) {
    const id = crypto.randomUUID()
    setDocuments((current) => [...current, { id, name: file.name, status: 'indexing' }])
    if (!isSupported(file)) {
      change(id, { status: 'failed', detail: 'Unsupported format' })
      return
    }
    try {
      const added = await uploadDocument(await conversation(), file)
      change(id, { status: 'ready', detail: `${added.chunks} passage${added.chunks > 1 ? 's' : ''}` })
    } catch (e) {
      change(id, { status: 'failed', detail: e instanceof Error ? e.message : 'Upload failed' })
    }
  }

  async function add(files: File[]) {
    for (const file of files)
      await upload(file)
  }

  function remove(id: string) {
    setDocuments((current) => current.filter((document) => document.id !== id))
  }

  function clear() {
    setDocuments([])
  }

  return { documents, add, remove, clear }
}
