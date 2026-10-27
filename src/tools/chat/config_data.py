##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## config_data
##

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ConfigData:
    model: str
    system_prompt: str
    spec_prompt: str
    question_prompt: str
    spec_path: str
    profiles_dir: str
    default_profile: str
    config_dir: str
    agents_path: str = "agents/agent.yaml"
    spec_think: bool | None = None
    response_format: dict | None = None
    max_loops: int = 10
    llm_settings: dict = field(default_factory=dict)
    think: bool | None = None
    ollama_provider: str = "auto"
    file_access_config: str = "file_access.yaml"
