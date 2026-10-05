from typing import Optional

from ..core.messages import SystemMessage


class Agent:
    def __init__(self, model: str, tools: list[str], prompt: SystemMessage):
        self._model = model
        self._tools = tools
        self._prompt = prompt
