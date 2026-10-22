##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## setup
##

from agent.agent import Agent
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
from tools.chat.prompts import SYSTEM_PROMPT, get_file_access_context
from tools.file_access.file_access import register_file_access_tools
from tools.file_access.workspace import WorkspaceSession
from tools.human_in_the_loop.mcp_server import (
    register_human_in_the_loop_tools,
)
from tools.sandbox.sandbox import create_sandbox_tools
from tools.search.web import create_search_tools
from tools.spec.spec import build_system_prompt


def read_api_key() -> str | None:
    key = Settings().ollama_api_key
    return key.get_secret_value() if key else None

def current_role(state: CliState, spec: str) -> SystemMessage:
    profile = state.current_profile()
    text = build_system_prompt(
        SYSTEM_PROMPT, build_profile_prompt(profile), spec
    ) + get_file_access_context(state.workspace)
    return SystemMessage(content=text)


def create_agent(state: CliState, tools: list[ITool], role: SystemMessage) -> Agent:
    tools_handler: ToolHandler = ToolHandler()
    tools_handler.register_many(tools)
    return Agent(
        name=state.current_profile().name,
        model=state.config.model,
        tools=[tool.name for tool in tools_handler.list_tools()],
        role=role,
        response_format=state.config.response_format,
        llm=state.llm,
        handler=tools_handler,
        max_loops=state.config.max_loops,
        think=state.config.think,
        on_chunk=state.display,
    )


def init_conversation(config: ConfigData) -> ConversationHandle:
    service = ConversationServiceFactory().create(ConversationStorage.MEMORY)
    conversation_id = service.create_conversation(
        user_id="local",
        system_prompt=config.system_prompt,
    )
    return ConversationHandle(service, conversation_id)


def create_cli_state(
    config: ConfigData,
    api_key: str | None,
    workspace: WorkspaceSession,
) -> CliState:
    active_profile = config.default_profile
    return CliState(
        config=config,
        profiles=init_profiles(config),
        active_profile=active_profile,
        display=ChunkDisplay(),
        llm=OllamaClient(
            config.model,
            api_key,
            options=config.llm_settings,
            provider=config.ollama_provider,
        ),
        conversation=init_conversation(config),
        workspace=workspace,
        human_answers=[],
    )


def create_tools(
    dependencies: ToolDependencies,
    workspace: WorkspaceSession,
    human_answers: list[dict[str, str]],
) -> list[ITool]:
    tools = create_search_tools()
    tools.extend(create_sandbox_tools(dependencies))

    tool_handler = ToolHandler()
    register_file_access_tools(tool_handler, workspace)
    register_human_in_the_loop_tools(tool_handler, human_answers)
    tools.extend(tool_handler.list_tools())
    return tools
