##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## setup
##

from agent.agent import Agent
from core.messages import SystemMessage
from core.tools import ToolHandler
from interfaces.cli.display import ChunkDisplay
from interfaces.cli.session_data import Session
from llm.ollama import OllamaClient
from tools.agent.profiles import build_profile_prompt, init_profiles
from tools.chat.config_data import ConfigData
from tools.chat.create_client import create_ollama_client
from tools.chat.settings import Settings
from tools.search.web import register_search_tools
from tools.spec.spec import build_system_prompt


def read_api_key() -> str | None:
    key = Settings().ollama_api_key
    return key.get_secret_value() if key else None


def current_role(session: Session, spec: str) -> SystemMessage:
    profile = session.current_profile()
    text = build_system_prompt(session.config.system_prompt, build_profile_prompt(profile), spec)
    return SystemMessage(content=text)


def create_agent(session: Session, api_key: str | None, role: SystemMessage) -> Agent:
    llm = OllamaClient(model=session.config.model, api_key=api_key, prompt=role)
    tools_handler = ToolHandler()
    register_search_tools(tools_handler)
    return Agent(
        name=session.current_profile()["name"],
        model=session.config.model,
        tools=[tool.name for tool in tools_handler.list_tools()],
        role=role,
        response_format=session.config.response_format,
        llm=llm,
        handler=tools_handler,
        max_loops=session.config.max_loops,
        on_chunk=session.display,
    )


def create_session(config: ConfigData, api_key: str | None) -> Session:
    active_profile = config.default_profile
    return Session(
        config=config,
        profiles=init_profiles(config),
        active_profile=active_profile,
        display=ChunkDisplay(),
        spec_client=create_ollama_client(config.model, api_key),
    )
