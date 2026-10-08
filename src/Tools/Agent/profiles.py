##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## profiles
##

from pathlib import Path

from src.Tools.Chat.module import fatal
from src.Tools.Chat.load_config import read_yaml, read_prompt

PROFILES_KEY = ("name", "role", "tone", "scope")

def validate_profile(file_path: Path, config: dict, required_keys: tuple[str, str, str]) -> bool:
    if not isinstance(config, dict):
        fatal(f"invalid profile format")
        return False
    missing = [key for key in required_keys if not config.get(key)]
    if missing:
        fatal(f"missing config keys: {', '.join(missing)} in file {file_path}")
        return False
    return True

def load_profile(config_dir: str, path: str) -> dict | None:
    profile = read_yaml(path)
    if not validate_profile(path, profile, PROFILES_KEY):
        return None
    if profile.get("prompt"):
        profile["prompt"] = read_prompt(config_dir, profile["prompt"])
    else:
        profile["prompt"] = ""
    if profile["prompt"] is None:
        return None
    return profile

def load_profiles(config_dir: str, profiles_dir: str) -> dict[str, dict] | None:
    files_path = Path(config_dir, profiles_dir).glob("*.yaml")
    profiles = {}
    for file_path in files_path:
        profile = load_profile(config_dir, file_path)
        if profile is None:
            return None
        profiles[file_path.stem] = profile
    if len(profiles) == 0:
        fatal(f"no profile available")
        return None
    return profiles

def build_profile_prompt(profile: dict) -> str:
    return f"""Agent profile
Your name is {profile["name"]}
Your role is {profile["role"]}
Your tone is {profile["tone"]}
Your scope is {profile["scope"]}

{profile["prompt"]}
"""