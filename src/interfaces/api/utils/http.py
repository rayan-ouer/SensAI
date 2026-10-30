##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## http
##

from queue import Queue
from threading import Thread

from fastapi import HTTPException, Request
from fastapi.responses import StreamingResponse

from core.conversation import ConversationNotFoundError, IConversationService
from core.types import MessageType
from interfaces.api.chat import create_agent, run_turn_safely, stream_events
from interfaces.api.schemas.input.conversation import MessageRequest
from interfaces.api.utils.models import available_models


def check_conversation(store: IConversationService, conversation_id: str) -> None:
    try:
        store.get_conversation_by_id(conversation_id)
    except ConversationNotFoundError:
        raise HTTPException(status_code=404, detail="Conversation not found")


def check_choices(body: MessageRequest, request: Request) -> None:
    if body.profile is not None and body.profile not in request.app.state.profiles:
        raise HTTPException(status_code=400, detail="Unknown profile")
    if body.model is not None and body.model not in available_models(request.app.state.config):
        raise HTTPException(status_code=400, detail="Unknown model")


def check_editable(store: IConversationService, conversation_id: str, message_id: str) -> None:
    check_conversation(store, conversation_id)
    history = store.get_used_history(conversation_id)
    if not any(message.id == message_id and message.role == MessageType.HUMAN for message in history):
        raise HTTPException(status_code=404, detail="Message not found")


def start_turn(
    request: Request,
    store: IConversationService,
    conversation_id: str,
    body: MessageRequest,
    edited_id: str | None,
) -> StreamingResponse:
    check_choices(body, request)
    events: Queue = Queue()
    agent = create_agent(request.app.state, events, body.profile, body.model)
    args = (agent, store, conversation_id, body.content, events, request.app.state, edited_id)
    Thread(target=run_turn_safely, args=args, daemon=True).start()
    return StreamingResponse(stream_events(events), media_type="application/x-ndjson")
