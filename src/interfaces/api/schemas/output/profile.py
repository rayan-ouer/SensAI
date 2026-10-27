##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## profile
##

from pydantic import BaseModel


class ProfileResponse(BaseModel):
    key: str
    name: str
    role: str


class ProfilesResponse(BaseModel):
    profiles: list[ProfileResponse]
    default: str
