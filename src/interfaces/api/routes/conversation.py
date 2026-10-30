##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## conversation
##

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from interfaces.api.dependencies import ConversationDep
from interfaces.api.schemas.input.conversation import CreateConversationRequest, MessageRequest
from interfaces.api.schemas.output.conversation import (
    CreateConversationResponse,
    MessagesResponse,
)
from interfaces.api.utils.http import check_conversation, check_editable, start_turn
from interfaces.api.utils.messages import is_displayed, to_message_response

conversation_router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
)


@conversation_router.post("/", response_model=CreateConversationResponse)
def create_conversation(
    body: CreateConversationRequest,
    request: Request,
    store: ConversationDep,
) -> CreateConversationResponse:
    conversation_id = store.create_conversation(
        user_id=body.user_id,
        system_prompt=request.app.state.config.system_prompt,
    )
    return CreateConversationResponse(id=conversation_id)


@conversation_router.post("/{conversation_id}/messages")
def send_message(
    conversation_id: str,
    body: MessageRequest,
    request: Request,
    store: ConversationDep,
) -> StreamingResponse:
    check_conversation(store, conversation_id)
    return start_turn(request, store, conversation_id, body, None)


@conversation_router.get("/{conversation_id}/messages", response_model=MessagesResponse)
def get_messages(conversation_id: str, store: ConversationDep) -> MessagesResponse:
    check_conversation(store, conversation_id)
    history = store.get_used_history(conversation_id)
    messages = [to_message_response(message) for message in history if is_displayed(message)]
    return MessagesResponse(messages=messages)


@conversation_router.put("/{conversation_id}/messages/{message_id}")
def edit_message(
    conversation_id: str,
    message_id: str,
    body: MessageRequest,
    request: Request,
    store: ConversationDep,
) -> StreamingResponse:
    check_editable(store, conversation_id, message_id)
    return start_turn(request, store, conversation_id, body, message_id)
