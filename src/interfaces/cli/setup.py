##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## setup
##

from pathlib import Path

from agent.agent import Agent
from agent.factory import AgentFactory
from agent.load import AgentsLoader
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
from tools.file_access.file_access import (
    build_workspace_context,
    create_file_access_tools,
    create_workspace,
)
from tools.human_in_the_loop.mcp_server import create_human_in_the_loop_tools
from tools.sandbox.sandbox import create_sandbox_tools
from tools.search.web import create_search_tools
from tools.spec.spec import build_system_prompt


def read_api_key() -> str | None:
    key = Settings().ollama_api_key
    return key.get_secret_value() if key else None


def current_role(state: CliState, spec: str) -> SystemMessage:
    if state.uses_agents_file:
        identity = state.entry_role
    else:
        identity = build_profile_prompt(state.current_profile())
    text = build_system_prompt(state.config.system_prompt, identity, spec)
    text += build_workspace_context(state.workspace)
    return SystemMessage(content=text)


def create_agent(state: CliState, tools: list[ITool], role: SystemMessage) -> Agent:
    registry = ToolHandler()
    registry.register_many(tools)
    agents_path = Path(state.config.config_dir, state.config.agents_path)
    agents_config = AgentsLoader.load(agents_path)
    if agents_config is not None:
        state.uses_agents_file = True
        entry = agents_config.by_name().get(agents_config.entry)
        state.entry_role = entry.role if entry is not None else ""
    else:
        agents_config = AgentsLoader.default(
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
    return agent


def init_conversation(config: ConfigData) -> ConversationHandle:
    service = ConversationServiceFactory().create(ConversationStorage.MEMORY)
    conversation_id = service.create_conversation(
        user_id="local",
        system_prompt=config.system_prompt,
    )
    return ConversationHandle(service, conversation_id)


def create_llm(config: ConfigData, api_key: str | None) -> OllamaClient:
    return OllamaClient(
        config.model,
        api_key,
        options=config.llm_settings,
        provider=config.ollama_provider,
    )


def create_cli_state(config: ConfigData, api_key: str | None) -> CliState:
    active_profile = config.default_profile
    return CliState(
        config=config,
        profiles=init_profiles(config),
        active_profile=active_profile,
        display=ChunkDisplay(),
        llm=create_llm(config, api_key),
        conversation=init_conversation(config),
        workspace=create_workspace(config),
    )


def create_tools(state: CliState) -> list[ITool]:
    dependencies = ToolDependencies(conversation_id=state.conversation.id)
    tools: list[ITool] = []
    tools.extend(create_search_tools())
    tools.extend(create_sandbox_tools(dependencies))
    tools.extend(create_file_access_tools(state.workspace))
    tools.extend(create_human_in_the_loop_tools(state.human_answers))
    return tools
