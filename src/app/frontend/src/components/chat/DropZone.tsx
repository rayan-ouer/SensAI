/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** DropZone
*/

// Icon from Lucide: https://lucide.dev/

import React, { useState } from 'react'
import { FileUp } from 'lucide-react'

type DropZoneProps = {
  children: React.ReactNode
  onDrop: (files: File[]) => void
}

function hasFiles(event: React.DragEvent): boolean {
  return event.dataTransfer.types.includes('Files')
}

function DropZone({ children, onDrop }: DropZoneProps) {
  const [dragging, setDragging] = useState(false)

  function handleDragOver(event: React.DragEvent) {
    if (!hasFiles(event))
      return
    event.preventDefault()
    setDragging(true)
  }

  function handleDragLeave(event: React.DragEvent) {
    if (!event.currentTarget.contains(event.relatedTarget as Node | null))
      setDragging(false)
  }

  function handleDrop(event: React.DragEvent) {
    if (!hasFiles(event))
      return
    event.preventDefault()
    setDragging(false)
    onDrop([...event.dataTransfer.files])
  }

  return (
    <div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className="relative flex min-w-0 flex-1 flex-col"
    >
      {children}
      {dragging && (
        <div className="pointer-events-none absolute inset-3 z-30 flex animate-in flex-col items-center justify-center gap-2 rounded-3xl border border-dashed border-amber-300/50 bg-black/70 text-amber-100 backdrop-blur-sm duration-150 fade-in">
          <FileUp className="size-7 text-amber-300" />
          <p className="text-sm">Drop your document, SensAI will use it in its answers</p>
          <p className="text-xs text-amber-100/50">PDF, Markdown, CSV or text</p>
        </div>
      )}
    </div>
  )
}

export default DropZone
