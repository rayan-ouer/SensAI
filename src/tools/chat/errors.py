##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## error
##

from pathlib import Path

class AppError(Exception):
    pass

class ConfigError(AppError):
    def __init__(self, message: str, config_path: str | Path):
        self.message = message
        self.config_path = config_path

    def __str__(self) -> str:
        return f"{self.message}: {self.config_path}"

class ProfileError(AppError):
    def __init__(self, message: str, profile_path: str | Path):
        self.message = message
        self.profile_path = profile_path

    def __str__(self):
        return f"{self.message}: {self.profile_path}"

class ModelNotFoundError(AppError):
    def __init__(self, model: str, detail: str | Path):
        self.model = model
        self.detail = detail

    def __str__(self):
        return f"{self.model}: {self.detail}"

class ChatError(AppError):
    pass
