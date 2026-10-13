##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## main
##

import argparse

from pydantic import ValidationError

from interfaces.cli.chat import agent_loop
from interfaces.cli.display import ChunkDisplay
from interfaces.cli.setup import create_agent, current_role, read_api_key
from Tools.Agent.profiles import init_profiles
from Tools.Chat.create_client import create_ollama_client
from Tools.Chat.errors import AppError
from Tools.Chat.load_config import load_config
from Tools.Chat.module import fatal
from Tools.Spec.spec import load_spec

def run():
    api_key = read_api_key()
    config = load_config(argparse.ArgumentParser())
    init_profiles(config)
    spec = load_spec(config["spec_path"])
    config["spec_client"] = create_ollama_client(config["model"], api_key)
    config["display"] = ChunkDisplay()
    agent = create_agent(config, api_key, current_role(config, spec))
    agent_loop(agent, config, spec)
    print("Bye bye")

def main():
    try:
        run()
    except (AppError, ValidationError) as e:
        fatal(e)

if __name__ == '__main__':
    main()
