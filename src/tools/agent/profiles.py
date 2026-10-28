##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## profiles
##

from dataclasses import fields
from pathlib import Path

from tools.agent.profile_data import ProfileData
from tools.chat.config_data import ConfigData
from tools.chat.errors import ProfileError
from tools.chat.load_config import read_prompt, read_yaml

PROFILES_KEY = ("name", "role", "tone", "scope")


def validate_profile(
    file_path: Path,
    config: dict,
    required_keys: tuple[str, str, str]
    ) -> None:
    if not isinstance(config, dict):
        raise ProfileError("invalid profile format", file_path)
    missing = [key for key in required_keys if not config.get(key)]
    if missing:
        raise ProfileError(f"missing profile keys: {', '.join(missing)}", file_path)


def load_profile(config_dir: str, path: str) -> ProfileData:
    profile = read_yaml(path)
    validate_profile(path, profile, PROFILES_KEY)
    names = {field.name for field in fields(ProfileData)}
    values = {key: value for key, value in profile.items() if key in names}
    if values.get("prompt"):
        values["prompt"] = read_prompt(config_dir, profile["prompt"])
    return ProfileData(**values)


def load_profiles(config_dir: str, profiles_dir: str) -> dict[str, ProfileData]:
    files_path = Path(config_dir, profiles_dir).glob("*.yaml")
    profiles = {}
    for file_path in files_path:
        profile = load_profile(config_dir, file_path)
        profiles[file_path.stem] = profile
    if len(profiles) == 0:
        raise ProfileError("no profile available", profiles_dir)
    return dict(sorted(profiles.items(), key=lambda item: (item[1].order, item[0])))


def init_profiles(config: ConfigData) -> dict[str, ProfileData]:
    profiles = load_profiles(config.config_dir, config.profiles_dir)
    if config.default_profile not in profiles:
        raise ProfileError(
            f"default profile '{config.default_profile}' not found",
            config.profiles_dir,
        )
    return profiles


def build_profile_prompt(profile: ProfileData) -> str:
    return f"""Agent profile
Your name is {profile.name}
Your role is {profile.role}
Your tone is {profile.tone}
Your scope is {profile.scope}

{profile.prompt}
"""
