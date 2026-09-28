from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum

from .tools import ToolCall

@dataclass_json
@dataclass
class IMessage:
    content: str | list[str | dict]
    type: str
    id: str

class SystemMessage(IMessage):
    type: str = "system"

class AIMessage(IMessage):
    type: str = "ai"
    tool_calls: list[ToolCall] = []

class HumanMessage(IMessage):
    type: str = "human"

class ToolStatus(Enum):
    SUCCESS = "success",
    ERROR = "error"

class ToolMessage(IMessage):
    type: str = "tool"
    status: ToolStatus = ToolStatus.SUCCESS
