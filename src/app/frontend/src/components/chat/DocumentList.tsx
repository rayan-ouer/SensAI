/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** DocumentList
*/

// Icons from Lucide: https://lucide.dev/

import { FileText, LoaderCircle, TriangleAlert, X } from 'lucide-react'

import type { UploadedDocument } from '@/types/chat'

type DocumentListProps = {
  documents: UploadedDocument[]
  onRemove: (id: string) => void
}

function StatusIcon({ status }: Pick<UploadedDocument, 'status'>) {
  if (status === 'indexing')
    return <LoaderCircle className="size-3.5 shrink-0 animate-spin" />
  if (status === 'failed')
    return <TriangleAlert className="size-3.5 shrink-0 text-red-300" />
  return <FileText className="size-3.5 shrink-0" />
}

function DocumentList({ documents, onRemove }: DocumentListProps) {
  if (documents.length === 0)
    return null
  return (
    <ul aria-label="Documents" className="mb-2 flex flex-wrap gap-1.5">
      {documents.map((document) => (
        <li
          key={document.id}
          title={document.detail}
          className="flex max-w-full items-center gap-1.5 rounded-full border border-white/10 bg-black/30 py-1 pr-1 pl-2.5 text-xs text-amber-100/70"
        >
          <StatusIcon status={document.status} />
          <span className="max-w-40 truncate">{document.name}</span>
          <span className={document.status === 'failed' ? 'max-w-48 truncate text-red-300' : 'whitespace-nowrap text-amber-100/40'}>
            {document.status === 'indexing' ? 'indexing...' : document.detail}
          </span>
          <button
            type="button"
            aria-label={`Remove ${document.name} from this list`}
            disabled={document.status === 'indexing'}
            onClick={() => onRemove(document.id)}
            className="rounded-full p-0.5 hover:bg-white/10 hover:text-amber-50 disabled:invisible"
          >
            <X className="size-3" />
          </button>
        </li>
      ))}
    </ul>
  )
}

export default DocumentList
