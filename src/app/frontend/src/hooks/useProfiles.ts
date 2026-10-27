/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** useProfiles
*/

import { useEffect, useState } from 'react'

import { fetchProfiles } from '@/services/chatApi'
import type { Profile } from '@/types/chat'

const STORAGE_KEY = 'sensai.profile'

function readStoredKey(): string | null {
  try {
    return localStorage.getItem(STORAGE_KEY)
  } catch {
    return null
  }
}

function storeKey(key: string) {
  try {
    localStorage.setItem(STORAGE_KEY, key)
  } catch {
    return
  }
}

export function useProfiles() {
  const [profiles, setProfiles] = useState<Profile[]>([])
  const [selected, setSelected] = useState<string | null>(null)

  useEffect(() => {
    fetchProfiles()
      .then((body) => {
        const stored = readStoredKey()
        const known = body.profiles.some((profile) => profile.key === stored)
        const isDefault = (profile: Profile) => Number(profile.key === body.default)
        setProfiles([...body.profiles].sort((a, b) => isDefault(b) - isDefault(a)))
        setSelected(known ? stored : body.default)
      })
      .catch(() => {})
  }, [])

  function select(key: string) {
    setSelected(key)
    storeKey(key)
  }

  return { profiles, selected, select }
}
