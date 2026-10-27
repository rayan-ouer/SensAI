##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## ollama
##

from collections.abc import Callable

import httpx

import ollama
from core.messages import AIMessage, IMessage
from core.tools import ITool
from llm.client import ILLMClient
from llm.errors import (
    LLMError,
    LLMModelNotFoundError,
    LLMTimeoutError,
    LLMUnreachableError,
)
from tools.chat.create_client import create_ollama_client

from .ollama_mappers import OllamaMapper
from .ollama_stream import StreamAccumulator, interrupted_message


def _raise_domain_error(error: BaseException):
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
    def __init__(
        self,
        model: str,
        api_key: str | None,
        prompt: IMessage | None = None,
        options: dict | None = None,
        provider: str = "auto",
    ):
        self._model = model  # the model to use
        self._prompt = prompt  # the prompt to use
        # a ollama client instance
        self._llm = create_ollama_client(model, api_key, provider=provider)
        self._thinking_support: dict[
            str, bool
        ] = {}  # a dictionary to cache the thinking support for each model
        self._options = options

    def chat(
        self,
        model: str,
        messages: list[IMessage],
        tools: list[ITool],
        response_format: dict | None,
        *,
        think: bool | None = None,
        include_thinking: bool = False,
        extract_thinking_tags: bool = False,
        on_chunk: Callable[[str, str], None] | None = None,
        is_cancelled: Callable[[], bool] | None = None,
    ) -> AIMessage:
        resolved_think = self._supports_thinking(model) if think is None else think
        accumulator = StreamAccumulator(on_chunk, is_cancelled, extract_thinking_tags)

        try:
            stream = self._llm.chat(
                model=model,
                messages=OllamaMapper.convert_messages(messages, include_thinking),
                tools=OllamaMapper.convert_tools(tools),
                stream=True,
                think=resolved_think,
                format=response_format,
                options=self._options,
            )
            return accumulator.consume(stream)
        except KeyboardInterrupt:
            return interrupted_message()
        except Exception as error:
            _raise_domain_error(error)

    # embed text into a vector
    def embed(self, embed_model: str | None, text: str) -> list[float]:
        try:
            response = self._llm.embed(model=embed_model or self._model, input=text)
        except Exception as error:
            _raise_domain_error(error)
        if not response.embeddings:
            return []
        return [float(value) for value in response.embeddings[0]]

    # check if the model supports thinking
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
