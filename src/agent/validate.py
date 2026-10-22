##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## validate
##

from collections import defaultdict
from collections.abc import Collection

from agent.definition import AgentDefinition, AgentsConfig


def _detect_cycles(agents: dict[str, AgentDefinition]) -> list[str]:
    """Return cycle descriptions using DFS (white/gray/black)."""
    white, gray, black = 0, 1, 2
    state = {name: white for name in agents}
    errors: list[str] = []

    def visit(name: str, stack: list[str]) -> None:
        state[name] = gray
        stack.append(name)
        for child in agents[name].agents:
            if child not in agents:
                continue
            if state[child] == gray:
                cycle_start = stack.index(child)
                cycle = stack[cycle_start:] + [child]
                errors.append(f"cycle detected: {' -> '.join(cycle)}")
            elif state[child] == white:
                visit(child, stack)
        stack.pop()
        state[name] = black

    for name in agents:
        if state[name] == white:
            visit(name, [])
    return errors


def validate_agents_config(
    config: AgentsConfig,
    available_tools: Collection[str],
) -> list[str]:
    errors: list[str] = []
    tool_set = set(available_tools)
    agents = config.by_name()

    seen: dict[str, int] = defaultdict(int)
    for agent in config.agents:
        seen[agent.name] += 1
    for name, count in seen.items():
        if count > 1:
            errors.append(f"duplicate agent name '{name}' ({count} definitions)")

    if config.entry not in agents:
        errors.append(f"entry agent '{config.entry}' is not defined")

    for agent in config.agents:
        for tool_name in agent.tools:
            if tool_name not in tool_set:
                errors.append(
                    f"agent '{agent.name}': unknown tool '{tool_name}'"
                )
            if tool_name in agents:
                errors.append(
                    f"agent '{agent.name}': '{tool_name}' is both a tool and an agent name; "
                    "put child agents under 'agents', not 'tools'"
                )

        for child_name in agent.agents:
            if child_name not in agents:
                errors.append(
                    f"agent '{agent.name}': unknown child agent '{child_name}'"
                )

        for name in sorted(set(agent.tools) & set(agent.agents)):
            errors.append(
                f"agent '{agent.name}': '{name}' listed in both 'tools' and 'agents'"
            )

    errors.extend(_detect_cycles(agents))
    return errors
