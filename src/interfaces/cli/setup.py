##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## setup
##

from typing import Optional

from agent.agent import Agent
from core.messages import SystemMessage
from core.tools import ToolHandler
from llm.client import ILLMClient
from llm.ollama import OllamaClient
from tools.agent.profiles import build_profile_prompt
from tools.chat.settings import Settings
from tools.search.web import register_search_tools
from tools.spec.spec import build_system_prompt
from core.tools import ITool, ToolHandler



def read_api_key() -> str | None:
    key = Settings().ollama_api_key
    return key.get_secret_value() if key else None

def current_role(config: dict, spec: str) -> SystemMessage:
    profile = config["profiles"][config["active_profile"]]
    text = build_system_prompt(config["system_prompt"], build_profile_prompt(profile), spec)
    return SystemMessage(content=text)

def create_agent(config: dict, tools: list[ITool], llm: ILLMClient) -> Agent:
    tools_handler: ToolHandler = ToolHandler()
    tools_handler.register_many(tools)
    print(config["system_prompt"])
    return Agent(
        name=config["profiles"][config["active_profile"]]["name"],
        model=config["model"],
        tools=[tool.name for tool in tools_handler.list_tools()],
        role=SystemMessage(content=config["system_prompt"]),
        llm=llm,
        handler=tools_handler,
        max_loops=config.get("max_loops", 10),
        on_chunk=config["display"],
    )