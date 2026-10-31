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
    config_path: str = Field(default="configs/local_config.yaml")
    conversation_storage: str = Field(default="memory")
    database_url: str | None = Field(default=None)
    monitor_db_path: str = Field(default="workspace/monitoring.sqlite3")
    vector_store: str = Field(default="sqlite")
    vector_db_path: str = Field(default="workspace/vectors.sqlite3")
