##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## cli_state
##

from dataclasses import dataclass

from interfaces.cli.conversation_handle import ConversationHandle
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
    llm: ILLMClient
    conversation: ConversationHandle

    def current_profile(self) -> ProfileData:
        return self.profiles[self.active_profile]
