from abc import ABC, abstractmethod
from typing import Callable, Optional

from core.messages import AIMessage, IMessage
from core.tools import ITool


class ILLMClient(ABC):
    @abstractmethod
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
        pass

    @abstractmethod
    def embed(self, embed_model: Optional[str], text: str) -> list[float]:
        pass
