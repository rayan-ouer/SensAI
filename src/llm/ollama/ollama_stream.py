import re
from typing import Any, Callable, Iterable, Optional

from core.messages import AIMessage
from core.tools import ToolCall
from llm.errors import LLMUnreachableError
from .ollama_mappers import parse_tool_call

OnChunk = Callable[[str, str], None]
IsCancelled = Callable[[], bool]

_THINKING_TAGS = re.compile(
    r"<(think|thinking)>(.*?)</\1>",
    re.IGNORECASE | re.DOTALL,
)

_METRICS = (
    "prompt_eval_count",
    "eval_count",
    "total_duration",
    "load_duration",
    "prompt_eval_duration",
    "eval_duration",
)


def interrupted_message(
    thinking_parts: Optional[list[str]] = None,
    content_parts: Optional[list[str]] = None,
) -> AIMessage:
    return AIMessage(
        content="".join(content_parts or []),
        tool_calls=[],
        thinking="".join(thinking_parts or []) or None,
        done_reason="interrupted",
        interrupted=True,
    )


def extract_thinking_tags(thinking: Optional[str], content: str) -> tuple[Optional[str], str]:
    matches = list(_THINKING_TAGS.finditer(content))
    if not matches:
        return thinking, content
    extracted = "\n".join(match.group(2).strip() for match in matches if match.group(2).strip())
    cleaned = _THINKING_TAGS.sub("", content).strip()
    if thinking and extracted:
        return f"{thinking}\n{extracted}", cleaned
    if extracted:
        return extracted, cleaned
    return thinking, cleaned


class StreamAccumulator:
    def __init__(
        self,
        on_chunk: Optional[OnChunk] = None,
        is_cancelled: Optional[IsCancelled] = None,
        extract_tags: bool = False,
    ):
        self._on_chunk = on_chunk
        self._is_cancelled = is_cancelled
        self._extract_tags = extract_tags
        self._thinking: list[str] = []
        self._content: list[str] = []
        self._tool_calls: list[ToolCall] = []
        self._done_reason: Optional[str] = None
        self._metrics: dict[str, Optional[int]] = {}
        self._done = False

    def consume(self, stream: Iterable[Any]) -> AIMessage:
        try:
            for chunk in stream:
                if self._is_cancelled is not None and self._is_cancelled():
                    return interrupted_message(self._thinking, self._content)
                self._add(chunk)
                if self._done:
                    break
        except KeyboardInterrupt:
            return interrupted_message(self._thinking, self._content)
        if not self._done:
            raise LLMUnreachableError("The model stream ended before completion")
        return self._build()

    def _add(self, chunk: Any) -> None:
        message = chunk.message
        if message.thinking:
            self._thinking.append(message.thinking)
            self._emit("thinking", message.thinking)
        if message.content:
            self._content.append(message.content)
            self._emit("content", message.content)
        if message.tool_calls:
            self._tool_calls.extend(parse_tool_call(call) for call in message.tool_calls)
        if chunk.done:
            self._done = True
            self._done_reason = chunk.done_reason
            self._metrics = {name: getattr(chunk, name, None) for name in _METRICS}

    def _emit(self, kind: str, text: str) -> None:
        if self._on_chunk is not None:
            self._on_chunk(kind, text)

    def _build(self) -> AIMessage:
        thinking = "".join(self._thinking) or None
        content = "".join(self._content)
        if self._extract_tags:
            thinking, content = extract_thinking_tags(thinking, content)
        return AIMessage(
            content=content,
            tool_calls=self._tool_calls,
            thinking=thinking,
            done_reason=self._done_reason,
            interrupted=False,
            **self._metrics,
        )
