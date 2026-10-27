##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## messages
##

from core.types import MessageType
from interfaces.api.schemas.output.conversation import MessageResponse


def is_displayed(message) -> bool:
    return message.role in (MessageType.HUMAN, MessageType.AI) and message.content != ""


def to_message_response(message) -> MessageResponse:
    if message.role == MessageType.HUMAN:
        return MessageResponse(role="user", content=message.content)
    return MessageResponse(role="assistant", content=message.content, thinking=message.thinking)
