##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## session_data
##

from dataclasses import dataclass, field

import ollama

from interfaces.cli.display import ChunkDisplay
from tools.chat.config_data import ConfigData


@dataclass
class Session:
    config: ConfigData
    profiles: dict[str, dict]
    active_profile: str
    display: ChunkDisplay
    spec_client: ollama.Client
    messages: list = field(default_factory=list)

    def current_profile(self) -> dict:
        return self.profiles[self.active_profile]
