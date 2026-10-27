/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** ProfileSelect
*/

import type { Profile } from '@/types/chat'

type ProfileSelectProps = {
  profiles: Profile[]
  selected: string | null
  disabled: boolean
  onSelect: (key: string) => void
}

function ProfileSelect({ profiles, selected, disabled, onSelect }: ProfileSelectProps) {
  if (profiles.length < 2)
    return null
  return (
    <div role="radiogroup" aria-label="Agent profile" className="flex rounded-full border border-white/10 bg-black/30 p-0.5">
      {profiles.map((profile) => (
        <button
          key={profile.key}
          type="button"
          role="radio"
          aria-checked={profile.key === selected}
          title={profile.role}
          disabled={disabled}
          onClick={() => onSelect(profile.key)}
          className="rounded-full px-2.5 py-0.5 text-xs text-amber-100/60 transition-colors hover:text-amber-50 disabled:cursor-not-allowed aria-checked:bg-amber-300 aria-checked:text-stone-950"
        >
          {profile.name}
        </button>
      ))}
    </div>
  )
}

export default ProfileSelect
