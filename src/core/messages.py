from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import Optional

from .tools import ToolCall
from core.types import MessageType, ToolStatus


@dataclass_json
@dataclass
class IMessage:
    content: str

    @property
    def role(self) -> MessageType:
        raise NotImplementedError


@dataclass_json
@dataclass
class HumanMessage(IMessage):
    @property
    def role(self) -> MessageType:
        return MessageType.HUMAN


@dataclass_json
@dataclass
class AIMessage(IMessage):
    tool_calls: list[ToolCall] = field(default_factory=list)
    thinking: Optional[str] = None
    prompt_eval_count: Optional[int] = None
    eval_count: Optional[int] = None
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_duration: Optional[int] = None
    done_reason: Optional[str] = None
    interrupted: bool = False
    truncated: bool = False

    @property
    def role(self) -> MessageType:
        return MessageType.AI


@dataclass_json
@dataclass
class SystemMessage(IMessage):
    @property
    def role(self) -> MessageType:
        return MessageType.SYSTEM


@dataclass_json
@dataclass
class ToolMessage(IMessage):
    tool_call_id: str
    tool_name: str
    result: dict
    status: ToolStatus = ToolStatus.SUCCESS

    @property
    def role(self) -> MessageType:
        return MessageType.TOOL
