from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from dataclasses_json import dataclass_json

from .types import ToolStatus


@dataclass_json
@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]
    status: ToolStatus = ToolStatus.PENDING
    result: dict[str, Any] | None = None


@dataclass
class ToolExecution:
    content: str
    result: dict[str, Any]
    status: ToolStatus


class ToolNotFoundError(Exception):
    def __init__(self, tool_name: str):
        self.tool_name = tool_name
        super().__init__(f"Tool '{tool_name}' is not registered.")


@dataclass()
class ToolDependencies:
    """Dependencies and context for tools."""

    conversation_id: str | None = None


class ITool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def args(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def run(self, arguments: dict[str, Any]) -> str:
        pass


class ToolHandler:
    def __init__(self) -> None:
        self._tools: dict[str, ITool] = {}

    def register(self, tool: ITool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered")
        self._tools[tool.name] = tool

    def register_many(self, tools: list[ITool]) -> None:
        for tool in tools:
            self.register(tool)

    def list_tools(self) -> list[ITool]:
        return list[ITool](self._tools.values())

    def get(self, name: str) -> ITool:
        tool = self._tools.get(name)
        if not tool:
            raise ToolNotFoundError(name)
        return tool

    def execute(self, call: ToolCall) -> ToolExecution:
        arguments: dict = call.arguments if isinstance(call.arguments, dict) else {}

        try:
            output = self.get(call.name).run(arguments)
        except ToolNotFoundError as error:
            return ToolExecution(
                content=str(error),
                result={"error": str(error)},
                status=ToolStatus.ERROR,
            )
        except Exception as error:
            message = str(error)
            return ToolExecution(
                content=message,
                result={"error": message},
                status=ToolStatus.ERROR,
            )
        return ToolExecution(
            content=output,
            result={"output": output},
            status=ToolStatus.SUCCESS,
        )
