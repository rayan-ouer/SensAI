##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## setup
##


from agent.agent import Agent
from core.messages import SystemMessage
from core.tools import ITool, ToolHandler
from llm.client import ILLMClient
from tools.agent.profiles import build_profile_prompt
from core.tools import ToolHandler
from interfaces.cli.cli_state import CliState
from interfaces.cli.display import ChunkDisplay
from llm.ollama import OllamaClient
from tools.agent.profiles import build_profile_prompt, init_profiles
from tools.chat.config_data import ConfigData
from tools.chat.settings import Settings
from tools.spec.spec import build_system_prompt


def read_api_key() -> str | None:
    key = Settings().ollama_api_key
    return key.get_secret_value() if key else None



def current_role(state: CliState, spec: str) -> SystemMessage:
    profile = state.current_profile()
    text = build_system_prompt(state.config.system_prompt, build_profile_prompt(profile), spec)
    return SystemMessage(content=text)


def create_agent(state: CliState, api_key: str | None, tools: list[ITool], role: SystemMessage) -> Agent:
    llm = OllamaClient(model=state.config.model, api_key=api_key, prompt=role)
    tools_handler: ToolHandler = ToolHandler()
    tools_handler.register_many(tools)

    return Agent(
        name=state.current_profile().name,
        model=state.config.model,
        tools=[tool.name for tool in tools_handler.list_tools()],
        role=role,
        response_format=state.config.response_format,
        llm=llm,
        handler=tools_handler,
        max_loops=state.config.max_loops,
        on_chunk=state.display,
    )
 
def create_cli_state(config: ConfigData, api_key: str | None) -> CliState:
    active_profile = config.default_profile
    return CliState(
        config=config,
        profiles=init_profiles(config),
        active_profile=active_profile,
        display=ChunkDisplay(),
        spec_llm=OllamaClient(config.model, api_key),
    )
