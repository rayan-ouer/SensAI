from collections.abc import Callable

from agent.agent import Agent
from agent.definition import AgentDefinition, AgentsConfig
from agent.validate import _reject_cycle, validate_agents_config
from core.dfs import dfs
from core.messages import SystemMessage
from core.tools import ToolHandler
from llm.client import ILLMClient
from tools.agent.agent_tool import AgentTool


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
        validate_agents_config(
            config,
            set([tool.name for tool in self._tools.list_tools()]),
        )

        order = self._build_graph(config)
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
    def _build_graph(config: AgentsConfig) -> list[str]:
        agents: dict[str, AgentDefinition] = config.by_name()
        return dfs(
            {name: definition.agents for name, definition in agents.items()},
            on_back_edge=_reject_cycle,
        )
