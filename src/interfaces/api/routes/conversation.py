from fastapi import APIRouter, Request

conversation_router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
)


@conversation_router.post("/")
async def create_conversation(request: Request):
    return {"message": "Hello, World!"}

