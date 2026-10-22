##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## definition
##

from dataclasses import dataclass, field


@dataclass(frozen=True)
class AgentDefinition:
    name: str
    description: str
    role: str
    model: str
    tools: list[str] = field(default_factory=list)
    agents: list[str] = field(default_factory=list)
    response_format: dict | None = None
    max_loops: int = 10


@dataclass(frozen=True)
class AgentsConfig:
    entry: str
    agents: list[AgentDefinition]

    def by_name(self) -> dict[str, AgentDefinition]:
        return {agent.name: agent for agent in self.agents}
