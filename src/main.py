##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## main
##

import argparse

from pydantic import ValidationError

from tools.chat.errors import AppError
from tools.chat.module import fatal, error
from tools.chat.settings import Settings
from tools.chat.load_config import load_config
from tools.chat.chat_loop import read_user_input
from tools.search.web import register_search_tools

from llm.ollama import OllamaClient
from llm.errors import LLMError
from agent.agent import Agent, AgentIterationLimitError
from core.messages import HumanMessage, IMessage, SystemMessage
from core.tools import ToolHandler


def display_chunk(kind: str, text: str) -> None:
    if kind in ("thinking", "content"):
        print(text, end="", flush=True)

def create_agent(config: dict, api_key: str | None) -> Agent:
    prompt = SystemMessage(content="Tu es un agent de recherche, tu as acces a des tools, utilise le tool web_search si tu n'est pas sur de la reponse.")
    llm = OllamaClient(model=config["model"], api_key=api_key, prompt=prompt)
    tools_handler = ToolHandler()
    register_search_tools(tools_handler)
    return Agent(
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

def agent_loop(agent: Agent):
    messages: list[IMessage] = []
    while True:
        user_input = read_user_input()
        if user_input is None or user_input == "/exit":
            break
        if not user_input:
            continue
        messages.append(HumanMessage(content=user_input))
        try:
            reply = agent.invoke(messages)
        except (LLMError, AgentIterationLimitError) as e:
            error(e)
            continue
        print(f"Content: {reply.content}")

def run():
    settings = Settings()
    key = settings.ollama_api_key
    api_key = key.get_secret_value() if key else None
    config = load_config(argparse.ArgumentParser())
    agent = create_agent(config, api_key)
    agent_loop(agent)
    print("Bye bye")

def main():
    try:
        run()
    except (AppError, ValidationError) as e:
        fatal(e)

if __name__ == '__main__':
    main()
