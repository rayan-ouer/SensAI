##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## load_config
##

import argparse
import yaml
import os
from typing import Optional

from Tools.Chat.errors import ConfigError

REQUIRED_KEYS = ("model", "system", "spec_prompt", "profiles_dir", "default_profile", "spec_path")
PROMPT_KEYS = ("system", "spec_prompt")

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

def validate_config(config: dict, required_keys: tuple[str, str, str], path: str):
    if not isinstance(config, dict):
        raise ConfigError("invalid config format", path)
    missing = [key for key in required_keys if not config.get(key)]
    if missing:
        raise ConfigError(f"missing config keys: {', '.join(missing)}", path)

def load_prompts(config_dir: str, config: dict):
    for key in PROMPT_KEYS:
        content = read_prompt(config_dir, config[key])
        config[key] = content

def load_config(parser: argparse.ArgumentParser) -> dict:
    parser.add_argument("-c", "--config", dest="config_opt", type=str, help="path to the yaml config file")
    args = parser.parse_args()
    config_path = args.config_opt or args.config
    if not config_path:
        parser.error("a config file is required (-c path or positional argument)")
    config = read_yaml(config_path)
    validate_config(config, REQUIRED_KEYS, config_path)
    config_dir = os.path.dirname(os.path.abspath(config_path))
    config["config_dir"] = config_dir
    load_prompts(config_dir, config)
    return config
