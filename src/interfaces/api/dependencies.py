##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## dependencies
##

from typing import Annotated

from fastapi import Depends, Request

from core.conversation import IConversationService


def get_conversation_service(request: Request) -> IConversationService:
    return request.app.state.conversations


ConversationDep = Annotated[IConversationService, Depends(get_conversation_service)]
