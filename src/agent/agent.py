import json
from collections.abc import Callable

from core.messages import AIMessage, IMessage, SystemMessage, ToolMessage
from core.tools import ToolCall, ToolExecution, ToolHandler
from core.types import MessageType
from llm.client import ILLMClient
from core.tools import ITool

class AgentIterationLimitError(Exception):
    def __init__(self, max_loops: int, message: AIMessage):
        self.max_loops = max_loops
        self.message = message
        super().__init__(f"Agent stopped after {max_loops} iterations")


class Agent:
    def __init__(
        self,
        name: str,  # the name of the agent
        model: str,  # the model to use
        tools: list[str],  # the tools to use
        role: SystemMessage,  # the role of the agent
        llm: ILLMClient,  # the llm client to use
        handler: ToolHandler,  # the tool handler to use
        response_format: dict | None = None,  # the response format to use
        max_loops: int = 10,  # the maximum number of loops to run
        think: bool | None = None,  # whether to think or not
        keep_thinking: bool = False,  # whether to keep thinking or not
        extract_thinking_tags: bool = False,  # whether to extract thinking tags or not
        on_chunk: Callable[[str, str], None]
        | None = None,  # the function to call when a chunk is received
        is_cancelled: Callable[[], bool]
        | None = None,  # the function to call to check if the agent is cancelled
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
            raise AgentIterationLimitError(
                self._max_loops, AIMessage(content="", truncated=True)
            )
        for index in range(self._max_loops):
            response: AIMessage = self._llm.chat(
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
                execution: ToolExecution = self.execute_tool(tool_call, self._handler)
                messages.append(
                    ToolMessage(
                        content=json.dumps(execution.result, ensure_ascii=False),
                        tool_call_id=tool_call.id,
                        tool_name=tool_call.name,
                        result=execution.result,
                        status=execution.status,
                    )
                )
        raise AgentIterationLimitError(
            self._max_loops, AIMessage(content="", truncated=True)
        )

    def set_role(self, role: SystemMessage) -> None:
        self._role = role

    def _ensure_role(self, messages: list[IMessage]) -> None:
        if messages and messages[0].role == MessageType.SYSTEM:
            messages[0] = self._role
        else:
            messages.insert(0, self._role)

    def _resolve_tools(self) -> list[ITool]:
        return [self._handler.get(name) for name in self._tools]
