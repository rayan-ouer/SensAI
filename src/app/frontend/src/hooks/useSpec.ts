/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** useSpec
*/

import { useEffect, useState } from 'react'

import { fetchSpec } from '@/services/chatApi'

export type SpecState = {
  spec: string
  updating: boolean
  startUpdate: () => void
  receive: (text: string) => void
  stopUpdate: () => void
}

export function useSpec(): SpecState {
  const [spec, setSpec] = useState('')
  const [updating, setUpdating] = useState(false)

  useEffect(() => {
    fetchSpec().then(setSpec).catch(() => {})
  }, [])

  return {
    spec,
    updating,
    startUpdate: () => setUpdating(true),
    receive: (text) => {
      setSpec(text)
      setUpdating(false)
    },
    stopUpdate: () => setUpdating(false),
  }
}
