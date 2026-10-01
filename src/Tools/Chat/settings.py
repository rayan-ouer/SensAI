##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## settings
##

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    ollama_api_key: SecretStr = None
    ollama_cloud_host: str = "https://ollama.com"
    ollama_local_host: str = "http://localhost:11434"

