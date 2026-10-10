from typing import Optional

from ollama import Client

from ..core.messages import SystemMessage, IMessage
from ..core.conversation import IConversation
from ..Tools.Chat.create_client import Settings
from ..Tools.Chat.create_client import create_ollama_client
from ..llm.client import LLMClient

class Agent:
    def __init__(self, name: str, model: str, tools: list[str], role: SystemMessage, response_format: dict, llm: LLMClient, max_loops: int = 10):
        self._name = name
        self._tools = tools
        self._prompt = role
        self._response_format = response_format
        self._llm = llm
        self._max_loops = max_loops

    def execute_tool(self):
        pass
    
    def invoke(self, messages: list[IMessage]):
        self._llm.chat(messages)
