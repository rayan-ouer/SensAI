##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## settings
##

from typing import Optional

from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from Tools.Chat.module import OLLAMA_CLOUD_HOST, OLLAMA_LOCAL_HOST

class Settings(BaseSettings):
    model_config: SettingsConfigDict = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    ollama_api_key: Optional[SecretStr] = Field(default=None)
    ollama_cloud_host: str = OLLAMA_CLOUD_HOST
    ollama_local_host: str = OLLAMA_LOCAL_HOST

