import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from memory.conversation.factory import ConversationFactory, ConversationStorage
from tools.chat.load_config import load_config_file
from tools.chat.settings import Settings

from .routes.conversation import conversation_router

logger = logging.getLogger(__name__)

VERSION_API: str = "v0.1.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    config = load_config_file(settings.config_path)
    app.state.settings = settings
    app.state.config = config
    app.state.conversation_store = ConversationFactory.create(ConversationStorage.MEMORY)
    logger.info("Config loaded from %s", settings.config_path)

    yield

    logger.info("Shutting down")


app = FastAPI(
    title="Sensai API",
    description="An master-wu harness for AI agents",
    version=VERSION_API,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}


@app.get("/version", tags=["version"])
async def version():
    return {"version": VERSION_API}


@app.get("/", tags=["root"])
async def root():
    return {"message": "Sensai API is running"}


app.include_router(conversation_router, prefix="/api", tags=["conversations"])
