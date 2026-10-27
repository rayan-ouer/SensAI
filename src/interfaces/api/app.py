##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## app
##

import asyncio
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from interfaces.api.setup import init_agent_resources
from memory.conversation.factory import ConversationServiceFactory, ConversationStorage
from tools.chat.load_config import ConfigLoader
from tools.chat.settings import Settings

from .routes.conversation import conversation_router

logger = logging.getLogger(__name__)

VERSION_API: str = "v0.1.0"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = Settings()
    app.state.conversations = ConversationServiceFactory().create(
        ConversationStorage(settings.conversation_storage)
    )
    config = ConfigLoader(settings.config_path).get_configs()
    app.state.settings = settings
    app.state.config = config
    await asyncio.to_thread(init_agent_resources, app.state, settings, config)
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
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/version", tags=["version"])
async def version() -> dict[str, str]:
    return {"version": VERSION_API}


@app.get("/", tags=["root"])
async def root() -> dict[str, str]:
    return {"message": "Sensai API is running"}


app.include_router(conversation_router, prefix="/api", tags=["conversations"])
