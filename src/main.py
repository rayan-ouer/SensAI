##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## main
##

import argparse
import sys
import ollama
from typing import Optional

from pydantic import ValidationError

from Tools.Chat.module import EXIT_S, EXIT_E
from Tools.Chat.settings import Settings
from Tools.Chat.send_user_prompt import send_user_prompt
from Tools.Chat.load_config import load_config
from Tools.Chat.create_client import create_ollama_client
from Tools.Wu.spec import load_spec, update_spec, save_spec, build_system_prompt

from llm.ollama import OllamaClient
from agent.agent import Agent
from core.messages import HumanMessage, SystemMessage
from core.tools import ToolHandler
from Tools.search.web import register_search_tools


def fatal(message: object):
    print(f"Error: {message}")
    sys.exit(EXIT_E)

def load_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as e:
        fatal(e)

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

def read_user_input() -> Optional[str]:
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
        fatal("API key expired or invalid")
    else:
        print(f"Error: {e.error}")

def ask_wu(messages: list, model: str, ollama_client_instance: ollama.Client) -> Optional[str]:
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
        new_spec = update_spec(ollama_client_instance, config["model"], config["spec_prompt"], spec, user_input, reply)
        save_spec(config["spec_path"], new_spec)
        return new_spec
    except (ollama.ResponseError, ConnectionError, OSError) as e:
        print(f"Warning: WU.md not updated: {e}")
    except KeyboardInterrupt:
        print()
        print("Warning: WU.md update interrupted")
    return spec

def run_turn(ollama_client_instance: ollama.Client, config: dict, messages: list, spec: str, user_input: str) -> str:
    messages.append({"role": "user", "content": user_input})
    messages[0]["content"] = build_system_prompt(config["system"], spec)
    reply = ask_wu(messages, config["model"], ollama_client_instance)
    if reply is None:
        return spec
    messages.append({"role": "assistant", "content": reply})
    return refresh_spec(ollama_client_instance, config, spec, user_input, reply)

def chat_loop(ollama_client_instance: ollama.Client, config: dict, spec: str):
    messages = [{"role": "system", "content": config["system"]}]
    while True:
        user_input = read_user_input()
        if user_input is None or user_input == "exit":
            break
        if user_input:
            spec = run_turn(ollama_client_instance, config, messages, spec, user_input)

def display_chunk(kind: str, text: str):
    if kind == "thinking":
        print(f"{kind}: {text}\n", end="", flush=True)

def main():
    settings: Settings = load_settings()
    config: dict = load_app_config()
    spec: str = load_spec(config["spec_path"])
    prompt: SystemMessage = SystemMessage(content="Tu es un agent de recherche, tu as acces a des tools, utilise le tool web_search si tu n'est pas sur de la reponse.")
    llm: OllamaClient = OllamaClient(model=config["model"], api_key=settings.ollama_api_key, prompt=prompt)
    tools_handler: ToolHandler = ToolHandler()
    register_search_tools(tools_handler)

    agent: Agent = Agent(
        name="Corporate agent",
        model=config["model"],
        tools=[tool.name for tool in tools_handler.list_tools()],
        role=prompt,
        response_format=config.get("response_format"),
        llm=llm,
        handler=tools_handler,
        max_loops=config.get("max_loops", 10),
        on_chunk=display_chunk,
    )
    messages = [HumanMessage(content="Quel est le nombre d'habitants du pays qui as gagné la coupe du monde de football 2026 ?")]
    reply = agent.invoke(messages)
    print(f"Content: {reply.content}")

if __name__ == '__main__':
    main()