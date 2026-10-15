##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## main
##

import argparse

from pydantic import ValidationError

from interfaces.cli.chat import agent_loop
from interfaces.cli.conversation_handle import ConversationHandle
from interfaces.cli.display import ChunkDisplay
from interfaces.cli.setup import create_agent, read_api_key
from llm.client import ILLMClient
from llm.ollama import OllamaClient
from memory.conversation.factory import ConversationServiceFactory, ConversationStorage
from tools.agent.profiles import init_profiles
from tools.chat.create_client import create_ollama_client
from tools.chat.errors import AppError
from tools.chat.load_config import load_config
from tools.chat.module import fatal
from tools.spec.spec import load_spec
from core.tools import ITool
from tools.mcp.adapter import MCPAdapter
from tools.mcp.client import MCPClient
from tools.search.web import create_search_server


def init_config():
    config = load_config(argparse.ArgumentParser())
    init_profiles(config)
    print(f"Starting {config['profiles'][config['active_profile']]['name']}")
    config["display"] = ChunkDisplay()
    return config


def init_spec(config: dict):
    return load_spec(config["spec_path"])


def init_llm(config: dict):
    model: str = config["model"]
    api_key = read_api_key()
    config["spec_client"] = create_ollama_client(model, api_key)
    return OllamaClient(model, api_key)


def init_conversation(config: dict) -> ConversationHandle:
    service = ConversationServiceFactory().create(ConversationStorage.MEMORY)
    conversation_id = service.create_conversation(
        user_id="local",
        system_prompt=config["system_prompt"],
    )
    return ConversationHandle(service, conversation_id)


def run():
    config = init_config()
    spec = init_spec(config)
    conversation = init_conversation(config)
    llm: ILLMClient = init_llm(config)
    mcp_tools = MCPAdapter(MCPClient(create_search_server()))
    tools: list[ITool] = list[ITool](mcp_tools.list_tools())
    agent = create_agent(config, tools, llm)
    agent_loop(agent, conversation, config, spec)
    print("Bye bye")


def main():
    try:
        run()
    except (AppError, ValidationError) as e:
        fatal(e)


if __name__ == "__main__":
    main()
