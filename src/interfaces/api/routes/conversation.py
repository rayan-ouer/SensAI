from fastapi import APIRouter, Request

from core.conversation import IConversation

conversation_router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
)


@conversation_router.post("/")
async def create_conversation(request: Request):
    store: IConversation = request.app.state.conversation_store
    conversation_id = store.create_conversation(
        system_prompt=request.app.state.config.get("system_prompt"),
    )
    return {"id": conversation_id}
