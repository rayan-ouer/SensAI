##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## load
##

from pathlib import Path
from typing import Any

import yaml

from agent.definition import AgentDefinition, AgentsConfig
from agent.errors import AgentConfigError


class AgentsLoader:
    @staticmethod
    def _strip_text(value: str, message: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise AgentConfigError(message)
        return stripped

    @staticmethod
    def _as_string_list(
        value: list[str], field_name: str, agent_name: str
    ) -> list[str]:
        items: list[str] = []

        for item in value:
            if not item.strip():
                raise AgentConfigError(
                    f"agent '{agent_name}': '{field_name}' entries must be non-empty strings"
                )
            items.append(item.strip())
        return items

    @staticmethod
    def _parse_agent(raw: dict, index: int) -> AgentDefinition:
        name = AgentsLoader._strip_text(
            raw.get("name", str()),
            f"agent at index {index}: 'name' is required",
        )
        description = AgentsLoader._strip_text(
            raw.get("description", str()),
            f"agent '{name}': 'description' is required",
        )
        role = AgentsLoader._strip_text(
            raw.get("role", str()),
            f"agent '{name}': 'role' is required",
        )
        model = AgentsLoader._strip_text(
            raw.get("model", str()),
            f"agent '{name}': 'model' is required",
        )
        tools = AgentsLoader._as_string_list(raw.get("tools"), "tools", name)
        children = AgentsLoader._as_string_list(raw.get("agents"), "agents", name)
        response_format: dict | None = raw.get("response_format", None)
        max_loops = raw.get("max_loops", 10)
        if max_loops < 1:
            raise AgentConfigError(
                f"agent '{name}': 'max_loops' must be a positive integer"
            )
        return AgentDefinition(
            name=name,
            description=description,
            role=role,
            model=model,
            tools=tools,
            agents=children,
            response_format=response_format,
            max_loops=max_loops,
        )

    @staticmethod
    def parse(data: dict[str, Any]) -> AgentsConfig:
        entry: str = AgentsLoader._strip_text(
            data.get("entry", str()),
            "missing or invalid 'entry' agent name",
        )
        raw_agents: list[dict] = data.get("agents", [])
        if not raw_agents:
            raise AgentConfigError("'agents' must not be empty")

        agents: list[AgentDefinition] = [
            AgentsLoader._parse_agent(raw, index)
            for index, raw in enumerate(raw_agents)
        ]
        return AgentsConfig(entry=entry, agents=agents)

    @staticmethod
    def load(path: str | Path) -> AgentsConfig | None:
        """Load agents config from YAML. Returns None if the file does not exist."""

        file_path = Path(path)
        if not file_path.is_file():
            return None
        try:
            with file_path.open("r", encoding="utf-8") as handle:
                data = yaml.safe_load(handle) or {}
        except yaml.YAMLError as error:
            raise AgentConfigError(
                f"failed to parse YAML: {error}", file_path
            ) from error

        try:
            return AgentsLoader.parse(data)
        except AgentConfigError as error:
            raise AgentConfigError(error.message, file_path) from error

    @staticmethod
    def default(
        *,
        model: str,
        role: str,
        tool_names: list[str],
        response_format: dict | None = None,
        max_loops: int = 10,
        name: str = "default",
        description: str = "Default conversational agent",
    ) -> AgentsConfig:
        return AgentsConfig(
            entry=name,
            agents=[
                AgentDefinition(
                    name=name,
                    description=description,
                    role=role,
                    model=model,
                    tools=list(tool_names),
                    agents=[],
                    response_format=response_format,
                    max_loops=max_loops,
                ),
            ],
        )
