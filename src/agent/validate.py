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


def _detect_cycles(agents: dict[str, AgentDefinition]) -> None:
    white, gray, black = 0, 1, 2
    state = {name: white for name in agents}

    def visit(name: str, stack: list[str]) -> None:
        state[name] = gray
        stack.append(name)
        for child in agents[name].agents:
            if child not in agents:
                continue
            if state[child] == gray:
                cycle_start = stack.index(child)
                cycle = stack[cycle_start:] + [child]
                raise AgentConfigError(f"cycle detected: {' -> '.join(cycle)}")
            elif state[child] == white:
                visit(child, stack)
        stack.pop()
        state[name] = black

    for name in agents:
        if state[name] == white:
            visit(name, [])


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


def validate_agents_config(
    config: AgentsConfig,
    available_tools: Collection[str],
) -> None:
    tool_set = set(available_tools)
    agents = config.by_name()

    seen: dict[str, int] = defaultdict(int)
    for agent in config.agents:
        seen[agent.name] += 1
    for name, count in seen.items():
        if count > 1:
            raise AgentConfigError(
                f"duplicate agent name '{name}' ({count} definitions)"
            )

    if config.entry not in agents:
        raise AgentConfigError(f"entry agent '{config.entry}' is not defined")

    for agent in config.agents:
        _validate_tools(agent, tool_set, agents)
        _validate_children(agent, agents)
        _validate_shared_names(agent)

    _detect_cycles(agents)
