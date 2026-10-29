##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## create_client
##


import ollama

from tools.chat.errors import ModelNotFoundError
from tools.chat.model_list import get_model_list

OLLAMA_LOCAL_HOST = "http://localhost:11434"
OLLAMA_CLOUD_HOST = "https://ollama.com"


def find_local_client(local_host: str, model: str) -> ollama.Client | None:
    local = ollama.Client(host=local_host)
    try:
        if model in get_model_list(local):
            return local
    except ConnectionError:
        pass
    return None


def create_cloud_client(cloud_host: str, api_key: str) -> ollama.Client:
    return ollama.Client(
        host=cloud_host, headers={"Authorization": f"Bearer {api_key}"}
    )


def find_cloud_client(cloud_host: str, model: str, api_key: str | None) -> ollama.Client:
    if not api_key:
        raise ModelNotFoundError(model, "not found locally and no API key was provided")
    cloud = create_cloud_client(cloud_host, api_key)
    if model in get_model_list(cloud):
        return cloud
    raise ModelNotFoundError(model, "not found neither locally nor in the cloud")


def create_ollama_client(
    model: str,
    api_key: str | None = None,
    provider: str = "auto",
) -> ollama.Client:
    if provider != "cloud":
        local = find_local_client(OLLAMA_LOCAL_HOST, model)
        if local is not None:
            return local
        if provider == "local":
            raise ModelNotFoundError(model, "not found locally")
    return find_cloud_client(OLLAMA_CLOUD_HOST, model, api_key)
