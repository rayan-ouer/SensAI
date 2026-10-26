from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from core.types import MessageType, ToolStatus

from .tools import ToolCall


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
    thinking: str | None = None
    prompt_eval_count: int | None = None
    eval_count: int | None = None
    total_duration: int | None = None
    load_duration: int | None = None
    prompt_eval_duration: int | None = None
    eval_duration: int | None = None
    done_reason: str | None = None
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
