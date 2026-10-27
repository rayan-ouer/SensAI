##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## conversation
##

from queue import Queue
from threading import Thread

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse

from core.conversation import ConversationNotFoundError
from core.types import MessageType
from interfaces.api.chat import create_agent, run_turn, stream_events
from interfaces.api.dependencies import ConversationDep
from interfaces.api.schemas.input.conversation import CreateConversationRequest, MessageRequest
from interfaces.api.schemas.output.conversation import (
    CreateConversationResponse,
    MessageResponse,
    MessagesResponse,
    StreamEvent,
)

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
    try:
        store.get_conversation_by_id(conversation_id)
    except ConversationNotFoundError:
        raise HTTPException(status_code=404, detail="Conversation not found")
    events: Queue = Queue()
    agent = create_agent(
        request.app.state,
        lambda kind, text: events.put(StreamEvent(type=kind, text=text)),
    )
    Thread(
        target=run_turn,
        args=(agent, store, conversation_id, body.content, events, request.app.state),
        daemon=True,
    ).start()
    return StreamingResponse(stream_events(events), media_type="application/x-ndjson")


def is_displayed(message) -> bool:
    return message.role in (MessageType.HUMAN, MessageType.AI) and message.content != ""


def to_message_response(message) -> MessageResponse:
    if message.role == MessageType.HUMAN:
        return MessageResponse(role="user", content=message.content)
    return MessageResponse(role="assistant", content=message.content, thinking=message.thinking)


@conversation_router.get("/{conversation_id}/messages", response_model=MessagesResponse)
def get_messages(conversation_id: str, store: ConversationDep) -> MessagesResponse:
    try:
        store.get_conversation_by_id(conversation_id)
    except ConversationNotFoundError:
        raise HTTPException(status_code=404, detail="Conversation not found")
    history = store.get_used_history(conversation_id)
    messages = [to_message_response(message) for message in history if is_displayed(message)]
    return MessagesResponse(messages=messages)
