##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## settings
##

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from src.Tools.Chat.module import OLLAMA_CLOUD_HOST, OLLAMA_LOCAL_HOST

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    ollama_api_key: SecretStr = None
    ollama_cloud_host: str = OLLAMA_CLOUD_HOST
    ollama_local_host: str = OLLAMA_LOCAL_HOST

