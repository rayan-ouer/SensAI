##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## setup
##

from fastapi.datastructures import State

from core.tools import ToolHandler
from llm.ollama.ollama import OllamaClient
from tools.agent.profiles import init_profiles
from tools.chat.config_data import ConfigData
from tools.chat.settings import Settings
from tools.search.web import create_search_tools


def init_agent_resources(state: State, settings: Settings, config: ConfigData):
    state.profiles = init_profiles(config)
    state.llm = OllamaClient(
        config.model,
        settings.ollama_api_key.get_secret_value() if settings.ollama_api_key else None,
        options=config.llm_settings,
    )
    state.tools = ToolHandler()
    state.tools.register_many(create_search_tools())
