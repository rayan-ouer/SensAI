##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## spec
##

from pydantic import BaseModel


class SpecResponse(BaseModel):
    content: str

