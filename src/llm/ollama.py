from typing import Optional

from ollama import Client

from .client import LLMClient
from ..Tools.Chat.create_client import create_ollama_client, Settings
from ..core.messages import IMessage


class OllamaClient(LLMClient):
    _llm: Client
    _model: str
    _host: str = "https://ollama.com"

    def __init__(self, model: str, api_key: Optional[str], prompt: Optional[IMessage]):
        super().__init__(model, api_key, prompt)

        if not api_key:
            self._host = "http://localhost:11434"
        settings = Settings(api_key=api_key, host=self._host)
        self._llm = create_ollama_client(settings, model)
    
    def run(self, prompt: Optional[IMessage], messages: list[IMessage]):
        return self._llm.chat(self._model, messages=messages, stream=True, think=True)
