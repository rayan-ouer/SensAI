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
from tools.agent.profiles import build_profile_prompt
from tools.chat.settings import Settings
from tools.chat.prompts import SYSTEM_PROMPT, get_file_access_context
from tools.file_access.file_access import register_file_access_tools
from tools.human_in_the_loop.mcp_server import (
    register_human_in_the_loop_tools,
)
from tools.search.web import register_search_tools
from tools.spec.spec import build_system_prompt


def read_api_key() -> str | None:
    key = Settings().ollama_api_key
    return key.get_secret_value() if key else None

def current_role(config: dict, spec: str) -> SystemMessage:
    profile = config["profiles"][config["active_profile"]]
    text = build_system_prompt(SYSTEM_PROMPT, build_profile_prompt(profile), spec) + get_file_access_context(config["file_access_workspace"])
    return SystemMessage(content=text)


def create_agent(config: dict, api_key: str | None, role: SystemMessage) -> Agent:
    llm = OllamaClient(model=config["model"], api_key=api_key, prompt=role,
        provider=config.get("ollama_provider", "auto"))
    tools_handler = ToolHandler()
    register_search_tools(tools_handler)
    register_file_access_tools(tools_handler, config["file_access_workspace"])
    config["human_answers"] = []
    register_human_in_the_loop_tools(tools_handler, config["human_answers"])
    return Agent(
        name=config["profiles"][config["active_profile"]]["name"],
        model=config["model"],
        tools=[tool.name for tool in tools_handler.list_tools()],
        role=role,
        response_format=config.get("response_format"),
        llm=llm,
        handler=tools_handler,
        max_loops=config.get("max_loops", 10),
        think=config.get("think", True),
        on_chunk=config["display"],
    )
