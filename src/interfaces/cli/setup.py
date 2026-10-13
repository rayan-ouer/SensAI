##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## setup
##

from agent.agent import Agent
from core.messages import SystemMessage
from core.tools import ToolHandler
from llm.ollama import OllamaClient
from Tools.Agent.profiles import build_profile_prompt
from Tools.Chat.settings import Settings
from Tools.search.web import register_search_tools
from Tools.Spec.spec import build_system_prompt

def read_api_key() -> str | None:
    key = Settings().ollama_api_key
    return key.get_secret_value() if key else None

def current_role(config: dict, spec: str) -> SystemMessage:
    profile = config["profiles"][config["active_profile"]]
    text = build_system_prompt(config["system_prompt"], build_profile_prompt(profile), spec)
    return SystemMessage(content=text)

def create_agent(config: dict, api_key: str | None, role: SystemMessage) -> Agent:
    llm = OllamaClient(model=config["model"], api_key=api_key, prompt=role)
    tools_handler = ToolHandler()
    register_search_tools(tools_handler)
    return Agent(
        name=config["profiles"][config["active_profile"]]["name"],
        model=config["model"],
        tools=[tool.name for tool in tools_handler.list_tools()],
        role=role,
        response_format=config.get("response_format"),
        llm=llm,
        handler=tools_handler,
        max_loops=config.get("max_loops", 10),
        on_chunk=config["display"],
    )
