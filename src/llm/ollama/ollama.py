from typing import Callable, NoReturn, Optional

import httpx
import ollama

from Tools.Chat.create_client import create_ollama_client
from Tools.Chat.settings import Settings
from core.messages import AIMessage, IMessage
from core.tools import ITool
from llm.client import ILLMClient
from llm.errors import (
    LLMError,
    LLMModelNotFoundError,
    LLMTimeoutError,
    LLMUnreachableError,
)
from .ollama_stream import StreamAccumulator, interrupted_message
from .ollama_mappers import convert_messages, convert_tools


def _raise_domain_error(error: BaseException) -> NoReturn:
    if isinstance(error, LLMError):
        raise error
    if isinstance(error, ollama.ResponseError):
        detail = str(getattr(error, "error", error))
        if error.status_code == 404 or "not found" in detail.lower():
            raise LLMModelNotFoundError(detail) from error
        raise LLMError(detail) from error
    if isinstance(error, (TimeoutError, httpx.TimeoutException)):
        raise LLMTimeoutError(str(error)) from error
    if isinstance(error, (ConnectionError, httpx.TransportError)):
        raise LLMUnreachableError(str(error)) from error
    raise error


class OllamaClient(ILLMClient):
    def __init__(self, model: str, api_key: Optional[str], prompt: Optional[IMessage] = None):
        self._model = model
        self._prompt = prompt
        self._host = "https://ollama.com"
        if not api_key:
            self._host = "http://localhost:11434"
        settings = Settings(ollama_api_key=api_key, ollama_cloud_host=self._host)
        self._llm = create_ollama_client(settings, model)
        self._thinking_support: dict[str, bool] = {}

    def chat(
        self,
        model: str,
        messages: list[IMessage],
        tools: list[ITool],
        response_format: Optional[dict],
        *,
        think: Optional[bool] = None,
        include_thinking: bool = False,
        extract_thinking_tags: bool = False,
        on_chunk: Optional[Callable[[str, str], None]] = None,
        is_cancelled: Optional[Callable[[], bool]] = None,
    ) -> AIMessage:
        resolved_think = self._supports_thinking(model) if think is None else think
        accumulator = StreamAccumulator(on_chunk, is_cancelled, extract_thinking_tags)

        try:
            stream = self._llm.chat(
                model=model,
                messages=convert_messages(messages, include_thinking),
                tools=convert_tools(tools),
                stream=True,
                think=resolved_think,
                format=response_format,
            )
            return accumulator.consume(stream)
        except KeyboardInterrupt:
            return interrupted_message()
        except Exception as error:
            _raise_domain_error(error)

    def embed(self, embed_model: Optional[str], text: str) -> list[float]:
        try:
            response = self._llm.embed(model=embed_model or self._model, input=text)
        except Exception as error:
            _raise_domain_error(error)
        if not response.embeddings:
            return []
        return [float(value) for value in response.embeddings[0]]

    def _supports_thinking(self, model: str) -> bool:
        cached = self._thinking_support.get(model)

        if cached is not None:
            return cached
        try:
            shown = self._llm.show(model)
            supported = "thinking" in (shown.capabilities or [])
        except Exception:
            supported = False
        self._thinking_support[model] = supported
        return supported
