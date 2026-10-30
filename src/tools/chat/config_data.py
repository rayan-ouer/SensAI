##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## config_data
##

from dataclasses import dataclass, field

PROMPT_VERSION_DIR = "prompt/versions"


@dataclass(frozen=True)
class ConfigData:
    model: str
    system_prompt: str
    spec_prompt: str
    question_prompt: str
    prompt_version: str
    spec_path: str
    profiles_dir: str
    default_profile: str
    config_dir: str
    spec_think: bool | None = None
    response_format: dict | None = None
    max_loops: int = 10
    llm_settings: dict = field(default_factory=dict)
    models: list[str] = field(default_factory=list)
    think: bool | None = None
    ollama_provider: str = "auto"
    file_access_config: str = "file_access.yaml"
    prompt_version_dir: str = PROMPT_VERSION_DIR
