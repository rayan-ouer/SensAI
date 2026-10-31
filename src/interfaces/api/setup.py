##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## setup
##

from fastapi.datastructures import State

from core.tools import ToolHandler
from llm.ollama.ollama import OllamaClient
from memory.vector.factory import VectorStoreKind
from monitoring.store import InteractionMonitor, MonitoredLLMClient, MonitoringStore
from tools.agent.profiles import init_profiles
from tools.chat.config_data import ConfigData
from tools.chat.settings import Settings
from tools.rag.tool import build_rag_resources, create_rag_tools
from tools.search.web import create_search_tools


def init_agent_resources(state: State, settings: Settings, config: ConfigData) -> None:
    state.profiles = init_profiles(config)
    llm = OllamaClient(
        config.model,
        settings.ollama_api_key.get_secret_value() if settings.ollama_api_key else None,
        options=config.llm_settings,
        provider=config.ollama_provider,
    )
    state.monitor = InteractionMonitor(MonitoringStore(settings.monitor_db_path))
    state.llm = MonitoredLLMClient(llm, state.monitor)
    state.vector_store, state.embedder, state.retriever = build_rag_resources(
        settings.vector_db_path,
        VectorStoreKind(settings.vector_store),
    )
    state.tools = ToolHandler()
    state.tools.register_many(create_search_tools())
    state.tools.register_many(create_rag_tools(state.retriever, state.embedder))
