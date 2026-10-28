##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## settings
##


from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )
    ollama_api_key: SecretStr | None = Field(default=None)
    ollama_cloud_host: str = Field(default="https://ollama.com")
    ollama_local_host: str = Field(default="http://localhost:11434")
    config_path: str = Field(default="configs/local_config.yaml")
    conversation_storage: str = Field(default="memory")
    database_url: str | None = Field(default=None)
