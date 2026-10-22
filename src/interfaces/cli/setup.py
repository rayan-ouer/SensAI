##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## setup
##

from pathlib import Path

from agent.agent import Agent
from agent.factory import AgentFactory
from agent.load import default_agents_config, load_agents_config
from core.messages import SystemMessage
from core.tools import ITool, ToolDependencies, ToolHandler
from interfaces.cli.cli_state import CliState
from interfaces.cli.conversation_handle import ConversationHandle
from interfaces.cli.display import ChunkDisplay
from llm.ollama import OllamaClient
from memory.conversation.factory import ConversationServiceFactory, ConversationStorage
from tools.agent.profiles import build_profile_prompt, init_profiles
from tools.chat.config_data import ConfigData
from tools.chat.settings import Settings
from tools.sandbox.sandbox import create_sandbox_tools
from tools.search.web import create_search_tools
from tools.spec.spec import build_system_prompt


def read_api_key() -> str | None:
    key = Settings().ollama_api_key
    return key.get_secret_value() if key else None


def current_role(state: CliState, spec: str) -> SystemMessage:
    profile = state.current_profile()
    text = build_system_prompt(state.config.system_prompt, build_profile_prompt(profile), spec)
    return SystemMessage(content=text)


def create_agent(state: CliState, tools: list[ITool], role: SystemMessage) -> Agent:
    registry = ToolHandler()
    registry.register_many(tools)
    agents_path = Path(state.config.config_dir, state.config.agents_path)
    agents_config = load_agents_config(agents_path)
    if agents_config is None:
        agents_config = default_agents_config(
            model=state.config.model,
            role=role.content,
            tool_names=[tool.name for tool in registry.list_tools()],
            response_format=state.config.response_format,
            max_loops=state.config.max_loops,
            name=state.current_profile().name,
            description=state.current_profile().role,
        )
    agent = AgentFactory(state.llm, registry).build(
        agents_config,
        on_chunk=state.display,
    )
    agent.set_role(role)
    return agent


def init_conversation(config: ConfigData) -> ConversationHandle:
    service = ConversationServiceFactory().create(ConversationStorage.MEMORY)
    conversation_id = service.create_conversation(
        user_id="local",
        system_prompt=config.system_prompt,
    )
    return ConversationHandle(service, conversation_id)


def create_cli_state(config: ConfigData, api_key: str | None) -> CliState:
    active_profile = config.default_profile
    return CliState(
        config=config,
        profiles=init_profiles(config),
        active_profile=active_profile,
        display=ChunkDisplay(),
        llm=OllamaClient(config.model, api_key, options=config.llm_settings),
        conversation=init_conversation(config),
    )


def create_tools(dependencies: ToolDependencies) -> list[ITool]:
    tools: list[ITool] = []
    tools.extend(create_search_tools())
    tools.extend(create_sandbox_tools(dependencies))
    return tools
