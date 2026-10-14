##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## main
##

import argparse

from pydantic import ValidationError

from core.conversation import IConversation
from interfaces.cli.chat import agent_loop
from interfaces.cli.display import ChunkDisplay
from interfaces.cli.setup import create_agent, current_role, read_api_key
from llm.client import ILLMClient
from llm.ollama import OllamaClient
from memory.conversation.factory import ConversationFactory, ConversationStorage
from tools.agent.profiles import init_profiles
from tools.chat.errors import AppError
from tools.chat.load_config import load_config
from tools.chat.module import fatal
from tools.spec.spec import load_spec

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
    return OllamaClient(model, api_key)

def run():
    config = init_config()
    spec = init_spec(config)
    conversation: IConversation = ConversationFactory.create(ConversationStorage.MEMORY)
    conversation.create_conversation(system_prompt=config["system_prompt"])
    llm: ILLMClient = init_llm(config)
    agent = create_agent(config, [], llm)
    agent_loop(agent, config, spec)
    print("Bye bye")


def main():
    try:
        run()
    except (AppError, ValidationError) as e:
        fatal(e)


if __name__ == "__main__":
    main()
