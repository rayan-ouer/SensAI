##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## settings
##


from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from tools.chat.module import OLLAMA_CLOUD_HOST, OLLAMA_LOCAL_HOST


class Settings(BaseSettings):
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )
    ollama_api_key: SecretStr | None = Field(default=None)
    ollama_cloud_host: str = OLLAMA_CLOUD_HOST
    ollama_local_host: str = OLLAMA_LOCAL_HOST
    config_path: str = Field(default="configs/local_config.yaml")
    conversation_storage: str = Field(default="memory")
    database_url: str | None = Field(default=None)
