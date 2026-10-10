from abc import ABC, abstractmethod
from typing import Optional

from ..core.conversation import IMessage, SystemMessage


class LLMClient(ABC):

    def __init__(self, model: str, api_key: Optional[str], prompt: Optional[IMessage]):
        self._model = model
        self._prompt = prompt

    @abstractmethod
    def chat(self, prompt: Optional[IMessage], messages: list[IMessage]):
        pass
