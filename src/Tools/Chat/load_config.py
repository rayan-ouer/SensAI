##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## load_config
##

import argparse
import yaml
import os

from src.Tools.Chat.module import EXIT_S, EXIT_E, fatal

REQUIRED_KEYS = ("model", "system", "spec_prompt", "profiles_dir", "default_profile", "spec_path")
PROMPT_KEYS = ("system", "spec_prompt")

def read_prompt(config_dir: str, relative_path: str) -> str | None:
    full_path = os.path.join(config_dir, relative_path)
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        fatal(f"prompt file not found : {full_path}")
        return None

def read_yaml(path: str) -> dict | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        fatal(f"config file not found : {path}")
    except yaml.YAMLError as e:
        fatal(f"failed to parse config file : {e}")
    return None

def validate_config(config: dict, required_keys: tuple[str, str, str]) -> bool:
    if not isinstance(config, dict):
        fatal(f"invalid config format")
        return False
    missing = [key for key in required_keys if not config.get(key)]
    if missing:
        fatal(f"missing config keys: {', '.join(missing)}")
        return False
    return True

def load_prompts(config_dir: str, config: dict) -> bool:
    for key in PROMPT_KEYS:
        content = read_prompt(config_dir, config[key])
        if content is None:
            return False
        config[key] = content
    return True

def load_config(parser: argparse.ArgumentParser) -> tuple[int, dict | None]:
    parser.add_argument("config", help="path to the yaml config file")
    args = parser.parse_args()
    config = read_yaml(args.config)
    if config is None or not validate_config(config, REQUIRED_KEYS):
        return EXIT_E, None
    config_dir = os.path.dirname(os.path.abspath(args.config))
    config["config_dir"] = config_dir
    if not load_prompts(config_dir, config):
        return EXIT_E, None
    return EXIT_S, config
