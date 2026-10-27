##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## conversation
##

from pydantic import BaseModel


class CreateConversationResponse(BaseModel):
    id: str


class StreamEvent(BaseModel):
    type: str
    text: str | None = None
    message: str | None = None
