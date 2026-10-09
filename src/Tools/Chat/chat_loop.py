##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## chat_loop
##

import ollama

from src.Tools.Chat.errors import ChatError
from src.Tools.Chat.module import error, warning
from src.Tools.Chat.send_user_prompt import send_user_prompt
from src.Tools.Chat.commands import handle_command
from src.Tools.Spec.spec import update_spec, save_spec, build_system_prompt
from src.Tools.Agent.profiles import build_profile_prompt

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
        raise ChatError(e)
    elif e.status_code == 401:
        raise ChatError("API key expired or invalid")
    else:
        error(f"{e.error}")

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
