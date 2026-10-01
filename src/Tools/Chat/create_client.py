##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## create_client
##

import ollama

from src.Tools.Chat.settings import Settings
from src.Tools.Chat.model_list import get_model_list

def find_local_client(settings: Settings, model: str) -> ollama.Client | None:
    local = ollama.Client(host=settings.ollama_local_host)
    try:
        if model in get_model_list(local):
            return local
    except ConnectionError:
        pass
    return None

def create_cloud_client(settings: Settings) -> ollama.Client:
    return ollama.Client(
        host=settings.ollama_cloud_host,
        headers={"Authorization": f"Bearer {settings.ollama_api_key.get_secret_value()}"}
    )

def create_ollama_client(settings: Settings, model: str) -> ollama.Client:
    local = find_local_client(settings, model)
    if local is not None:
        return local
    if settings.ollama_api_key is None:
        raise ValueError(f"Model '{model}' not found locally and OLLAMA_API_KEY is not set")
    cloud = create_cloud_client(settings)
    if model in get_model_list(cloud):
        return cloud
    raise ValueError(f"Model '{model}' not found neither locally nor in the cloud")
