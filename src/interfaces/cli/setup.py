##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## setup
##

from agent.agent import Agent
from core.messages import SystemMessage
from core.tools import ITool, ToolHandler
from interfaces.cli.cli_state import CliState
from interfaces.cli.conversation_handle import ConversationHandle
from interfaces.cli.display import ChunkDisplay
from llm.ollama import OllamaClient
from memory.conversation.factory import ConversationServiceFactory, ConversationStorage
from tools.agent.profiles import build_profile_prompt, init_profiles
from tools.chat.config_data import ConfigData
from tools.chat.settings import Settings
from tools.mcp.adapter import MCPAdapter
from tools.mcp.client import MCPClient
from tools.search.web import create_search_server
from tools.spec.spec import build_system_prompt


def read_api_key() -> str | None:
    key = Settings().ollama_api_key
    return key.get_secret_value() if key else None


def current_role(state: CliState, spec: str) -> SystemMessage:
    profile = state.current_profile()
    text = build_system_prompt(state.config.system_prompt, build_profile_prompt(profile), spec)
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
        on_chunk=state.display,
    )


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


def create_tools() -> list[ITool]:
    mcp_tools = MCPAdapter(MCPClient(create_search_server()))
    tools: list[ITool] = list[ITool](mcp_tools.list_tools())
    return tools
