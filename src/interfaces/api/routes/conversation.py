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
from pydantic import BaseModel

from core.conversation import ConversationNotFoundError
from interfaces.api.chat import create_agent, run_turn, stream_events
from interfaces.api.dependencies import ConversationDep

conversation_router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
)


class CreateConversationRequest(BaseModel):
    user_id: str


@conversation_router.post("/")
def create_conversation(
    body: CreateConversationRequest,
    request: Request,
    store: ConversationDep,
):
    conversation_id = store.create_conversation(
        user_id=body.user_id,
        system_prompt=request.app.state.config.system_prompt,
    )
    return {"id": conversation_id}


class MessageRequest(BaseModel):
    content: str


@conversation_router.post("/{conversation_id}/messages")
def send_message(
    conversation_id: str,
    body: MessageRequest,
    request: Request,
    store: ConversationDep,
):
    try:
        store.get_conversation_by_id(conversation_id)
    except ConversationNotFoundError:
        raise HTTPException(status_code=404, detail="Conversation not found")
    events: Queue = Queue()
    agent = create_agent(
        request.app.state,
        lambda kind, text: events.put({"type": kind, "text": text}),
    )
    Thread(
        target=run_turn,
        args=(agent, store, conversation_id, body.content, events),
        daemon=True,
    ).start()
    return StreamingResponse(stream_events(events), media_type="application/x-ndjson")
