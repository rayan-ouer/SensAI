##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## cli_state
##

from dataclasses import dataclass, field

from interfaces.cli.display import ChunkDisplay
from llm.client import ILLMClient
from tools.agent.profile_data import ProfileData
from tools.chat.config_data import ConfigData


@dataclass
class CliState:
    config: ConfigData
    profiles: dict[str, ProfileData]
    active_profile: str
    display: ChunkDisplay
    spec_llm: ILLMClient
    messages: list = field(default_factory=list)

    def current_profile(self) -> ProfileData:
        return self.profiles[self.active_profile]
