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


def _as_string_list(value: Any, field_name: str, agent_name: str, errors: list[str]) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        errors.append(f"agent '{agent_name}': '{field_name}' must be a list of strings")
        return []
    items: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            errors.append(
                f"agent '{agent_name}': '{field_name}' entries must be non-empty strings"
            )
            continue
        items.append(item.strip())
    return items


def _parse_agent(raw: Any, index: int, errors: list[str]) -> AgentDefinition | None:
    if not isinstance(raw, dict):
        errors.append(f"agent at index {index}: must be a mapping")
        return None

    name = raw.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append(f"agent at index {index}: missing or invalid 'name'")
        name = f"<invalid:{index}>"

    description = raw.get("description", "")
    if description is not None and not isinstance(description, str):
        errors.append(f"agent '{name}': 'description' must be a string")
        description = ""

    role = raw.get("role")
    if not isinstance(role, str) or not role.strip():
        errors.append(f"agent '{name}': missing or invalid 'role'")
        role = ""

    model = raw.get("model")
    if not isinstance(model, str) or not model.strip():
        errors.append(f"agent '{name}': missing or invalid 'model'")
        model = ""

    tools = _as_string_list(raw.get("tools"), "tools", name, errors)
    children = _as_string_list(raw.get("agents"), "agents", name, errors)

    response_format = raw.get("response_format")
    if response_format is not None and not isinstance(response_format, dict):
        errors.append(f"agent '{name}': 'response_format' must be a mapping")
        response_format = None
    if isinstance(response_format, dict) and not response_format:
        response_format = None

    max_loops = raw.get("max_loops", 10)
    if not isinstance(max_loops, int) or isinstance(max_loops, bool) or max_loops < 1:
        errors.append(f"agent '{name}': 'max_loops' must be a positive integer")
        max_loops = 10

    return AgentDefinition(
        name=name.strip() if isinstance(name, str) else name,
        description=(description or "").strip(),
        role=role.strip() if isinstance(role, str) else role,
        model=model.strip() if isinstance(model, str) else model,
        tools=tools,
        agents=children,
        response_format=response_format,
        max_loops=max_loops,
    )


def parse_agents_config(data: Any) -> tuple[AgentsConfig | None, list[str]]:
    errors: list[str] = []
    if data is None:
        return None, ["config is empty"]
    if not isinstance(data, dict):
        return None, ["config root must be a mapping with 'entry' and 'agents'"]

    entry = data.get("entry")
    if not isinstance(entry, str) or not entry.strip():
        errors.append("missing or invalid 'entry' agent name")
        entry = ""

    raw_agents = data.get("agents")
    if not isinstance(raw_agents, list):
        errors.append("'agents' must be a list")
        return None, errors
    if not raw_agents:
        errors.append("'agents' must not be empty")

    agents: list[AgentDefinition] = []
    for index, raw in enumerate(raw_agents):
        definition = _parse_agent(raw, index, errors)
        if definition is not None:
            agents.append(definition)

    if errors:
        return None, errors

    return (
        AgentsConfig(entry=entry.strip(), agents=agents),
        [],
    )


def load_agents_config(path: str | Path) -> AgentsConfig | None:
    """Load agents config from YAML. Returns None if the file does not exist."""
    file_path = Path(path)
    if not file_path.is_file():
        return None

    try:
        with file_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except yaml.YAMLError as error:
        raise AgentConfigError([f"failed to parse YAML: {error}"], file_path) from error

    config, errors = parse_agents_config(data)
    if errors:
        raise AgentConfigError(errors, file_path)
    return config


def default_agents_config(
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
