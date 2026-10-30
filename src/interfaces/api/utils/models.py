##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## models
##

from tools.chat.config_data import ConfigData


def available_models(config: ConfigData) -> list[str]:
    if not config.models:
        return [config.model]
    return config.models
