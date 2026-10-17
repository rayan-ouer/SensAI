##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## load_config
##

import os
from dataclasses import fields

import yaml

from tools.chat.config_data import ConfigData
from tools.chat.errors import ConfigError


REQUIRED_KEYS = (
    "model",
    "system_prompt",
    "spec_prompt",
    "profiles_dir",
    "default_profile",
    "spec_path",
)

PROMPT_KEYS = ("system_prompt", "spec_prompt")


def read_prompt(config_dir: str, relative_path: str) -> str:
    full_path = os.path.join(config_dir, relative_path)
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise ConfigError("prompt file not found", full_path)


def read_yaml(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise ConfigError("config file not found", path)
    except yaml.YAMLError as e:
        raise ConfigError("failed to parse config file", e)


class ConfigLoader:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config_dir = os.path.dirname(os.path.abspath(config_path))

    def validate_config(self, config: dict):
        if not isinstance(config, dict):
            raise ConfigError("invalid config format", self.config_path)
        missing = [key for key in REQUIRED_KEYS if not config.get(key)]
        if missing:
            raise ConfigError(f"missing config keys: {', '.join(missing)}", self.config_path)

    def get_configs(self) -> ConfigData:
        config = read_yaml(self.config_path)
        self.validate_config(config)
        names = {field.name for field in fields(ConfigData)}
        values = {key: value for key, value in config.items() if key in names}
        for key in PROMPT_KEYS:
            values[key] = read_prompt(self.config_dir, config[key])
        values["config_dir"] = self.config_dir
        return ConfigData(**values)
