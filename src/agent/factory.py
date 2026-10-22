##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## factory
##

from collections import defaultdict, deque
from collections.abc import Callable

from agent.agent import Agent
from tools.agent.agent_tool import AgentTool
from agent.definition import AgentDefinition, AgentsConfig
from agent.errors import AgentConfigError
from agent.validate import validate_agents_config
from core.messages import SystemMessage
from core.tools import ITool, ToolHandler
from llm.client import ILLMClient


class AgentFactory:
    def __init__(self, llm: ILLMClient, tools: ToolHandler):
        self._tools = tools
        self._llm = llm

    def build(
        self,
        config: AgentsConfig,
        *,
        on_chunk: Callable[[str, str], None] | None = None,
        is_cancelled: Callable[[], bool] | None = None,
        think: bool | None = None,
        keep_thinking: bool = False,
        extract_thinking_tags: bool = False,
    ) -> Agent:
        errors = validate_agents_config(
            config,
            [tool.name for tool in self._tools.list_tools()],
        )
        if errors:
            raise AgentConfigError(errors)

        order = self._build_order(config)
        built: dict[str, Agent] = {}
        definitions = config.by_name()

        for name in order:
            definition = definitions[name]
            is_entry = name == config.entry
            built[name] = self._build_agent(
                definition,
                built,
                on_chunk=on_chunk if is_entry else None,
                is_cancelled=is_cancelled if is_entry else None,
                think=think,
                keep_thinking=keep_thinking,
                extract_thinking_tags=extract_thinking_tags,
            )

        return built[config.entry]

    def _build_agent(
        self,
        definition: AgentDefinition,
        built: dict[str, Agent],
        *,
        on_chunk: Callable[[str, str], None] | None,
        is_cancelled: Callable[[], bool] | None,
        think: bool | None,
        keep_thinking: bool,
        extract_thinking_tags: bool,
    ) -> Agent:
        handler = ToolHandler()
        tool_names: list[str] = []

        for tool_name in definition.tools:
            handler.register(self._tools.get(tool_name))
            tool_names.append(tool_name)

        for child_name in definition.agents:
            child_agent = built[child_name]
            handler.register(AgentTool(child_agent))
            tool_names.append(child_name)

        return Agent(
            name=definition.name,
            description=definition.description,
            model=definition.model,
            tools=tool_names,
            role=SystemMessage(content=definition.role),
            llm=self._llm,
            handler=handler,
            response_format=definition.response_format,
            max_loops=definition.max_loops,
            think=think,
            keep_thinking=keep_thinking,
            extract_thinking_tags=extract_thinking_tags,
            on_chunk=on_chunk,
            is_cancelled=is_cancelled,
        )

    @staticmethod
    def _build_order(config: AgentsConfig) -> list[str]:
        """Topological order: children before parents."""
        agents = config.by_name()
        indegree = {name: 0 for name in agents}
        dependents: dict[str, list[str]] = defaultdict(list)

        for name, definition in agents.items():
            for child in definition.agents:
                if child not in agents:
                    continue
                # edge child -> parent (child must be built first)
                dependents[child].append(name)
                indegree[name] += 1

        queue = deque(sorted(name for name, degree in indegree.items() if degree == 0))
        order: list[str] = []
        while queue:
            name = queue.popleft()
            order.append(name)
            for parent in sorted(dependents[name]):
                indegree[parent] -= 1
                if indegree[parent] == 0:
                    queue.append(parent)

        if len(order) != len(agents):
            # Cycles are reported by validate; keep a clear fallback.
            missing = sorted(set(agents) - set(order))
            raise AgentConfigError(
                [f"cannot order agents due to cycle involving: {', '.join(missing)}"]
            )
        return order
