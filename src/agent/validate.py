##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## validate
##

from collections import defaultdict
from collections.abc import Collection

from agent.definition import AgentDefinition, AgentsConfig
from agent.errors import AgentConfigError
from core.dfs import dfs


def _reject_cycle(cycle: list[str]) -> None:
    raise AgentConfigError(f"cycle detected: {' -> '.join(cycle)}")

def _validate_tools(
    agent: AgentDefinition,
    tool_set: set[str],
    agents: dict[str, AgentDefinition],
) -> None:
    for tool_name in agent.tools:
        if tool_name not in tool_set:
            raise AgentConfigError(f"agent '{agent.name}': unknown tool '{tool_name}'")
        if tool_name in agents:
            raise AgentConfigError(
                f"agent '{agent.name}': '{tool_name}' is both a tool and an agent name; "
                "put child agents under 'agents', not 'tools'"
            )


def _validate_children(
    agent: AgentDefinition,
    agents: dict[str, AgentDefinition],
) -> None:
    for child_name in agent.agents:
        if child_name not in agents:
            raise AgentConfigError(
                f"agent '{agent.name}': unknown child agent '{child_name}'"
            )


def _validate_shared_names(agent: AgentDefinition) -> None:
    for name in sorted(set(agent.tools) & set(agent.agents)):
        raise AgentConfigError(
            f"agent '{agent.name}': '{name}' listed in both 'tools' and 'agents'"
        )


def _validate_duplicates(agents: dict[str, AgentDefinition]) -> None:
    seen: dict[str, int] = {}

    for agent in agents.values():
        seen[agent.name] = seen.get(agent.name, 0) + 1
        if seen[agent.name] > 1:
            raise AgentConfigError(
                f"duplicate agent name '{agent.name}' ({seen[agent.name]} definitions)"
            )

def validate_agents_config(
    config: AgentsConfig,
    available_tools: set[str],
) -> None:
    agents: dict[str, AgentDefinition] = config.by_name()

    if config.entry not in agents:
        raise AgentConfigError(f"entry agent '{config.entry}' is not defined")
    _validate_duplicates(agents)
    for agent in config.agents:
        _validate_tools(agent, available_tools, agents)
        _validate_children(agent, agents)
        _validate_shared_names(agent)
    dfs(
        {name: agent.agents for name, agent in agents.items()},
        on_back_edge=_reject_cycle,
    )
