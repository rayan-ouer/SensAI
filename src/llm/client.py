from abc import ABC, abstractmethod
from collections.abc import Callable

from core.messages import AIMessage, IMessage
from core.tools import ITool


class ILLMClient(ABC):
    @abstractmethod
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
        pass

    @abstractmethod
    def embed(self, embed_model: str | None, text: str) -> list[float]:
        pass
