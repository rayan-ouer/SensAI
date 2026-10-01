from enum import Enum

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from .tools import ToolCall
from app.core.types import MessageType, ToolStatus



@dataclass
@dataclass_json
class IMessage:
    id: str
    content: str

    @property
    def role(self) -> MessageType:
        raise NotImplementedError


@dataclass
class HumanMessage(IMessage):

    @property
    def role(self) -> MessageType:
        return MessageType.HUMAN


@dataclass
class AIMessage(IMessage):

    tool_calls: list[ToolCall] = field(default_factory=list)

    @property
    def role(self) -> MessageType:
        return MessageType.AI


@dataclass
class SystemMessage(IMessage):

    @property
    def role(self) -> MessageType:
        return MessageType.SYSTEM


@dataclass
class ToolMessage(IMessage):

    tool_call_id: str
    tool_name: str
    result: dict
    status: ToolStatus = ToolStatus.SUCCESS

    @property
    def role(self) -> MessageType:
        return MessageType.TOOL