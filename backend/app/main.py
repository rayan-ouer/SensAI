##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## main
##

import argparse
import sys
import ollama

from pydantic import ValidationError

from src.Tools.Chat.module import EXIT_S, EXIT_E, fatal, warning

from src.Tools.Chat.settings import Settings
from src.Tools.Chat.send_user_prompt import send_user_prompt
from src.Tools.Chat.load_config import load_config
from src.Tools.Chat.create_client import create_ollama_client
from src.Tools.Spec.spec import load_spec, update_spec, save_spec, build_system_prompt
from src.Tools.Agent.profiles import load_profiles, build_profile_prompt
from src.Tools.Chat.commands import handle_command

def load_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as e:
        fatal(e)

def load_app_profiles(config: dict):
    profiles = load_profiles(config["config_dir"], config["profiles_dir"])
    if profiles is None:
        sys.exit(EXIT_E)
    if config["default_profile"] not in profiles:
        fatal(f"default profile '{config["default_profile"]}' not found")
    config["profiles"] = profiles
    config["active_profile"] = config["default_profile"]

def load_app_config() -> dict:
    ret, config = load_config(argparse.ArgumentParser())
    if ret != EXIT_S:
        sys.exit(ret)
    return config

def get_client(settings: Settings, model: str) -> ollama.Client:
    try:
        return create_ollama_client(settings, model)
    except ValueError as e:
        fatal(e)

def read_user_input() -> str | None:
    print("> ", end="", flush=True)
    try:
        return input()
    except (EOFError, KeyboardInterrupt):
        print()
        return None

def handle_chat_error(e: BaseException):
    if isinstance(e, KeyboardInterrupt):
        print()
        print("Interrupted by user")
    elif isinstance(e, ConnectionError):
        fatal(e)
    elif e.status_code == 401:
        fatal(f"API key expired or invalid")
    else:
        fatal(f"{e.error}")

def ask_agent(messages: list, model: str, ollama_client_instance: ollama.Client) -> str | None:
    try:
        reply = send_user_prompt(messages, model, ollama_client_instance)
    except (ollama.ResponseError, ConnectionError, KeyboardInterrupt) as e:
        handle_chat_error(e)
        messages.pop()
        return None
    print()
    return reply

def refresh_spec(ollama_client_instance: ollama.Client, config: dict, spec: str, user_input: str, reply: str) -> str:
    try:
        new_spec = update_spec(ollama_client_instance, config["model"], config["spec_prompt"], spec, user_input, reply, config.get("spec_think"))
        save_spec(config["spec_path"], new_spec)
        return new_spec
    except (ollama.ResponseError, ConnectionError, OSError) as e:
        warning(f"{config["spec_path"]} not updated: {e}")
    except KeyboardInterrupt:
        print()
        warning(f"{config["spec_path"]} update interrupted")
    return spec

def run_turn(ollama_client_instance: ollama.Client, config: dict, messages: list, spec: str, user_input: str) -> str:
    messages.append({"role": "user", "content": user_input})
    messages[0]["content"] = build_system_prompt(config["system"], build_profile_prompt(config["profiles"][config["active_profile"]]), spec)
    reply = ask_agent(messages, config["model"], ollama_client_instance)
    if reply is None:
        return spec
    messages.append({"role": "assistant", "content": reply})
    return refresh_spec(ollama_client_instance, config, spec, user_input, reply)


def chat_loop(ollama_client_instance: ollama.Client, config: dict, spec: str):
    messages = [{"role": "system", "content": config["system"]}]
    config["messages"] = messages
    while True:
        user_input = read_user_input()
        if user_input is None or user_input == "/exit":
            break
        if user_input.startswith("/"):
            handle_command(config, user_input)
        elif user_input:
            spec = run_turn(ollama_client_instance, config, messages, spec, user_input)

def main():
    settings = load_settings()
    config = load_app_config()
    load_app_profiles(config)
    spec = load_spec(config["spec_path"])
    ollama_client_instance = get_client(settings, config["model"])
    chat_loop(ollama_client_instance, config, spec)
    print()
    print("Bye bye")

if __name__ == '__main__':
    main()
