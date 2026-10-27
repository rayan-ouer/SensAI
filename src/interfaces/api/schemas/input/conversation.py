##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## conversation
##

from pydantic import BaseModel


class CreateConversationRequest(BaseModel):
    user_id: str


class MessageRequest(BaseModel):
    content: str
    profile: str | None = None
