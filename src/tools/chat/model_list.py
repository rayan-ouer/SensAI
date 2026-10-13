##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## model_list
##

import ollama


def get_model_list(ollama_client_instance: ollama.Client) -> list[str]:
    return sorted(entry.model for entry in ollama_client_instance.list().models)
