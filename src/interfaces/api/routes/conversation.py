from fastapi import APIRouter, Request
from pydantic import BaseModel

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
        system_prompt=request.app.state.config.get("system_prompt"),
    )
    return {"id": conversation_id}
