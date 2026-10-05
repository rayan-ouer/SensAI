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

from Tools.Chat.module import EXIT_S, EXIT_E

REQUIRED_KEYS = ("model", "system", "spec_prompt")
PROMPT_KEYS = ("system", "spec_prompt")
DEFAULT_SPEC_PATH = "workspace/WU.md"

def read_prompt(config_dir: str, relative_path: str) -> Optional[str]:
    full_path = os.path.join(config_dir, relative_path)
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: prompt file not found : {full_path}")
        return None

def read_yaml(path: str) -> Optional[dict]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: config file not found : {path}")
    except yaml.YAMLError as e:
        print(f"Error: failed to parse config file : {e}")
    return None

def validate_config(config: dict) -> bool:
    if not isinstance(config, dict):
        print("Error: invalid config format")
        return False
    missing = [key for key in REQUIRED_KEYS if config.get(key) is None]
    if missing:
        print(f"Error: missing config keys: {', '.join(missing)}")
        return False
    return True

def load_prompts(config_dir: str, config: dict) -> bool:
    for key in PROMPT_KEYS:
        content = read_prompt(config_dir, config[key])
        if content is None:
            return False
        config[key] = content
    return True

def load_config(parser: argparse.ArgumentParser) -> tuple[int, Optional[dict]]:
    parser.add_argument("-c", dest="config", type=str, help="path to the yaml config file")
    args = parser.parse_args()
    config = read_yaml(args.config)
    if config is None or not validate_config(config):
        return EXIT_E, None
    config.setdefault("spec_path", DEFAULT_SPEC_PATH)
    config_dir = os.path.dirname(os.path.abspath(args.config))
    if not load_prompts(config_dir, config):
        return EXIT_E, None
    return EXIT_S, config
