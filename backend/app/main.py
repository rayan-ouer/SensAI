##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## main
##

import argparse

from pydantic import ValidationError

from src.Tools.Chat.errors import AppError
from src.Tools.Chat.module import fatal
from src.Tools.Chat.settings import Settings
from src.Tools.Chat.load_config import load_config
from src.Tools.Chat.create_client import create_ollama_client
from src.Tools.Chat.chat_loop import chat_loop
from src.Tools.Spec.spec import load_spec
from src.Tools.Agent.profiles import init_profiles

def run():
    settings = Settings()
    key = settings.ollama_api_key
    api_key = key.get_secret_value() if key else None
    config = load_config(argparse.ArgumentParser())
    init_profiles(config)
    spec = load_spec(config["spec_path"])
    ollama_client_instance = create_ollama_client(
        config["model"],
        api_key,
        settings.ollama_local_host,
        settings.ollama_cloud_host
        )
    chat_loop(ollama_client_instance, config, spec)
    print()
    print("Bye bye")

def main():
    try:
        run()
    except (AppError, ValidationError) as e:
        fatal(e)

if __name__ == '__main__':
    main()
