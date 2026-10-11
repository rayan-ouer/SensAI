import json
from typing import Callable, Optional

from core.messages import AIMessage, IMessage, SystemMessage, ToolMessage
from core.tools import ToolCall, ToolExecution, ToolHandler
from core.types import MessageType
from llm.client import ILLMClient


class AgentIterationLimitError(Exception):
    def __init__(self, max_loops: int, message: AIMessage):
        self.max_loops = max_loops
        self.message = message
        super().__init__(f"Agent stopped after {max_loops} iterations")


class Agent:
    def __init__(
        self,
        name: str,
        model: str,
        tools: list[str],
        role: SystemMessage,
        response_format: Optional[dict],
        llm: ILLMClient,
        handler: ToolHandler,
        max_loops: int = 10,
        think: Optional[bool] = None,
        keep_thinking: bool = False,
        extract_thinking_tags: bool = False,
        on_chunk: Optional[Callable[[str, str], None]] = None,
        is_cancelled: Optional[Callable[[], bool]] = None,
    ):
        self._name = name
        self._model = model
        self._tools = tools
        self._role = role
        self._response_format = response_format
        self._llm = llm
        self._handler = handler
        self._max_loops = max_loops
        self._think = think
        self._keep_thinking = keep_thinking
        self._extract_thinking_tags = extract_thinking_tags
        self._on_chunk = on_chunk
        self._is_cancelled = is_cancelled

    def execute_tool(self, tool_call: ToolCall, handler: ToolHandler) -> ToolExecution:
        return handler.execute(tool_call)

    def invoke(self, messages: list[IMessage]) -> AIMessage:
        self._ensure_role(messages)
        if self._max_loops < 1:
            raise AgentIterationLimitError(self._max_loops, AIMessage(content="", truncated=True))
        for index in range(self._max_loops):
            response = self._llm.chat(
                self._model,
                messages,
                self._resolve_tools(),
                self._response_format,
                think=self._think,
                include_thinking=self._keep_thinking,
                extract_thinking_tags=self._extract_thinking_tags,
                on_chunk=self._on_chunk,
                is_cancelled=self._is_cancelled,
            )
            if response.interrupted:
                response.tool_calls = []
                messages.append(response)
                return response
            if response.tool_calls and index == self._max_loops - 1:
                response.truncated = True
                messages.append(response)
                raise AgentIterationLimitError(self._max_loops, response)
            messages.append(response)
            if not response.tool_calls:
                return response
            for tool_call in response.tool_calls:
                execution = self.execute_tool(tool_call, self._handler)
                messages.append(ToolMessage(
                    content=json.dumps(execution.result, ensure_ascii=False),
                    tool_call_id=tool_call.id,
                    tool_name=tool_call.name,
                    result=execution.result,
                    status=execution.status,
                ))
        raise AgentIterationLimitError(self._max_loops, AIMessage(content="", truncated=True))

    def _ensure_role(self, messages: list[IMessage]) -> None:
        if messages and messages[0].role == MessageType.SYSTEM and messages[0].content == self._role.content:
            return
        messages.insert(0, self._role)

    def _resolve_tools(self) -> list:
        return [self._handler.get(name) for name in self._tools]
