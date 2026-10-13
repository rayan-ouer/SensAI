##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## main
##

import argparse

from agent.agent import Agent, AgentIterationLimitError
from core.messages import HumanMessage, IMessage, SystemMessage
from core.tools import ToolHandler
from llm.errors import LLMError
from llm.ollama import OllamaClient
from memory.vector.sqlite.sqlite_store import SQLiteStore
from tools.chat.chat_loop import read_user_input
from tools.chat.load_config import load_config
from tools.chat.module import error
from tools.chat.settings import Settings
from tools.loader.loader import FileReader
from tools.rag.chunker.chunker import Chunker
from tools.rag.embedder.embedding import embed_chunks
from tools.search.web import register_search_tools


def display_chunk(kind: str, text: str) -> None:
    if kind in ("thinking", "content"):
        print(text, end="", flush=True)


def create_agent(config: dict, api_key: str | None) -> Agent:
    prompt = SystemMessage(config["system"])
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
    print("Starting Master Wu")
    settings = Settings()
    key = settings.ollama_api_key
    api_key = key.get_secret_value() if key else None
    config = load_config(argparse.ArgumentParser())
    agent = create_agent(config, api_key)
    agent_loop(agent)
    print("Bye bye")


#def main():
#    fr = FileReader("files/convention.pdf")
#    chunks = Chunker(fr.documents()).chunk()
#    embedded = embed_chunks(chunks)
#    store = SQLiteStore("memory.db")
#    store.add(embedded)
#    results = store.search("What is the main character of the book?", 1)
#    print(results)

def main():
    run()

if __name__ == "__main__":
    main()
