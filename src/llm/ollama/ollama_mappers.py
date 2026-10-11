import json
import uuid
from typing import Any, Callable, Optional

from core.messages import AIMessage, HumanMessage, IMessage, SystemMessage, ToolMessage
from core.tools import ITool, ToolCall

MessageConverter = Callable[[Any, bool], dict[str, Any]]


def _convert_human(message: HumanMessage, include_thinking: bool) -> dict[str, Any]:
    return {"role": "user", "content": message.content}


def _convert_system(message: SystemMessage, include_thinking: bool) -> dict[str, Any]:
    return {"role": "system", "content": message.content}

def _convert_ai(message: AIMessage, include_thinking: bool) -> dict[str, Any]:
    payload: dict[str, Any] = {"role": "assistant", "content": message.content}

    if message.tool_calls:
        payload["tool_calls"] = [
            {"function": {"name": call.name, "arguments": call.arguments}}
            for call in message.tool_calls
        ]
    if include_thinking and message.thinking:
        payload["thinking"] = message.thinking
    return payload


def _convert_tool_result(message: ToolMessage, include_thinking: bool) -> dict[str, Any]:
    return {
        "role": "tool",
        "content": json.dumps(message.result, ensure_ascii=False),
        "tool_name": message.tool_name,
    }


_MESSAGE_CONVERTERS: dict[type[IMessage], MessageConverter] = {
    HumanMessage: _convert_human,
    SystemMessage: _convert_system,
    AIMessage: _convert_ai,
    ToolMessage: _convert_tool_result,
}


def convert_message(message: IMessage, include_thinking: bool) -> dict[str, Any]:
    converter = _MESSAGE_CONVERTERS.get(type(message))
    if converter is None:
        raise ValueError(f"Unsupported message type: {type(message).__name__}")
    return converter(message, include_thinking)


def convert_messages(messages: list[IMessage], include_thinking: bool) -> list[dict[str, Any]]:
    return [convert_message(message, include_thinking) for message in messages]


def convert_tool(tool: ITool) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.args,
        },
    }


def convert_tools(tools: list[ITool]) -> Optional[list[dict[str, Any]]]:
    if not tools:
        return None
    return [convert_tool(tool) for tool in tools]


def _parse_arguments(raw: Any) -> dict[str, Any]:
    arguments = raw.function.arguments
    if isinstance(arguments, str):
        if not arguments:
            return {}
        parsed = json.loads(arguments)
        return parsed if isinstance(parsed, dict) else {"value": parsed}
    if not arguments:
        return {}
    return dict(arguments)


def parse_tool_call(raw: Any) -> ToolCall:
    call_id = getattr(raw, "id", None) or uuid.uuid4().hex
    return ToolCall(id=str(call_id), name=raw.function.name, arguments=_parse_arguments(raw))
