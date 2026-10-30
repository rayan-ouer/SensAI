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
    options: list[str] | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


class MessageResponse(BaseModel):
    role: str
    content: str
    thinking: str | None = None


class MessagesResponse(BaseModel):
    messages: list[MessageResponse]
