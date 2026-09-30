##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## load_config
##

import argparse
import yaml
import os

from src.Tools.Chat.module import EXIT_S, EXIT_E

def read_prompt(config_dir: str, relative_path: str) -> str | None:
    full_path = os.path.join(config_dir, relative_path)
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: prompt file not found : {full_path}")
        return None

def load_config(parser: argparse.ArgumentParser) -> tuple[int, dict | None]:
    parser.add_argument("config", help="path to the yaml config file")

    args = parser.parse_args()

    try:
        with open(args.config, "r") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: config file not found : {args.config}")
        return EXIT_E, None
    except yaml.YAMLError as e:
        print(f"Error: failed to parse config file : {e}")
        return EXIT_E, None

    if not isinstance(config, dict):
        print("Error: invalid config format")
        return EXIT_E, None

    required_keys = ["model", "system", "spec_prompt"]
    config.setdefault("spec_path", "workspace/WU.md")
    missing = [key for key in required_keys if config.get(key) is None]
    if missing:
        print(f"Error: missing config keys: {', '.join(missing)}")
        return EXIT_E, None

    config_dir = os.path.dirname(os.path.abspath(args.config))

    for key in required_keys[1:]:
        content = read_prompt(config_dir, config[key])
        if content is None:
            return EXIT_E, None
        config[key] = content

    return EXIT_S, config
