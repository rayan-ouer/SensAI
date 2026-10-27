from typing import Any

from agent.agent import Agent, AgentIterationLimitError, AgentTurn
from core.messages import HumanMessage
from core.tools import ITool


class AgentTool(ITool):
    """Expose a child agent as a regular tool to its parent."""

    def __init__(self, agent: Agent):
        self._agent = agent

    @property
    def name(self) -> str:
        return self._agent.name

    @property
    def description(self) -> str:
        names = ", ".join(self._agent.tool_names)
        if names == str():
            return self._agent.description
        return f"{self._agent.description} It can call: {names}."

    @property
    def args(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": (
                        "Instruction or question for the agent. "
                        "It runs with a fresh history and returns only its final answer."
                    ),
                },
            },
            "required": ["task"],
        }

    def run(self, arguments: dict[str, Any]) -> str:
        task: str = arguments.get("task")

        try:
            turn: AgentTurn = self._agent.invoke([HumanMessage(content=task.strip())])
        except AgentIterationLimitError as error:
            content = error.message.content if error.message else str()
            if content != str():
                return content
            raise
        return turn.reply.content
