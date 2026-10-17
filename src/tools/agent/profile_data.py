##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## profile_data
##

from dataclasses import dataclass


@dataclass(frozen=True)
class ProfileData:
    name: str
    role: str
    tone: str
    scope: str
    prompt: str = ""
