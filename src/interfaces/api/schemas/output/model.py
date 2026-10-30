##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## model
##

from pydantic import BaseModel


class ModelsResponse(BaseModel):
    models: list[str]
    default: str
