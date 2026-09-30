##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## create_client
##

import ollama
import sys

from src.Tools.Chat.module import EXIT_E

def ollama_client(config: dict[str, str], ollama_api_key: str) -> ollama.Client:
    if config.get("host"):
        if not ollama_api_key:
            print("Error: OLLAMA_API_KEY environment variable not set.")
            sys.exit(EXIT_E)
        return ollama.Client(
            host=config["host"],
            headers={"Authorization": f"Bearer {ollama_api_key}"}
            )
    return ollama.Client()
