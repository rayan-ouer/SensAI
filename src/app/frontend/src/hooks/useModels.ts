/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** useModels
*/

import { useEffect, useState } from 'react'

import { fetchModels } from '@/services/chatApi'

const STORAGE_KEY = 'sensai.model'

function readStoredModel(): string | null {
  try {
    return localStorage.getItem(STORAGE_KEY)
  } catch {
    return null
  }
}

function storeModel(model: string) {
  try {
    localStorage.setItem(STORAGE_KEY, model)
  } catch {
    return
  }
}

export function useModels() {
  const [models, setModels] = useState<string[]>([])
  const [selected, setSelected] = useState<string | null>(null)

  useEffect(() => {
    fetchModels()
      .then((body) => {
        const stored = readStoredModel()
        setModels(body.models)
        setSelected(stored !== null && body.models.includes(stored) ? stored : body.default)
      })
      .catch(() => {})
  }, [])

  function select(model: string) {
    setSelected(model)
    storeModel(model)
  }

  return { models, selected, select }
}
