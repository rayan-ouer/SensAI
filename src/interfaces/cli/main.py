##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## main
##

import argparse

from pydantic import ValidationError

from interfaces.cli.chat import agent_loop
from interfaces.cli.display import ChunkDisplay
from interfaces.cli.setup import create_agent, current_role, read_api_key
from tools.agent.profiles import init_profiles
from tools.chat.create_client import create_ollama_client
from tools.chat.errors import AppError
from tools.chat.load_config import load_config
from tools.chat.module import fatal
from tools.spec.spec import load_spec


def run():
    print("Starting Master Wu")
    api_key = read_api_key()
    config = load_config(argparse.ArgumentParser())
    init_profiles(config)
    spec = load_spec(config["spec_path"])
    config["spec_client"] = create_ollama_client(config["model"], api_key)
    config["display"] = ChunkDisplay()
    agent = create_agent(config, api_key, current_role(config, spec))
    agent_loop(agent, config, spec)
    print("Bye bye")


def vector_store_demo():
    from memory.vector.sqlite.sqlite_store import SQLiteStore
    from tools.loader.loader import FileReader
    from tools.rag.chunker.chunker import Chunker
    from tools.rag.embedder.embedding import embed_chunks

    fr = FileReader("files/convention.pdf")
    chunks = Chunker(fr.documents()).chunk()
    embedded = embed_chunks(chunks)
    store = SQLiteStore("memory.db")
    store.add(embedded)
    results = store.search("What is the main character of the book?", 1)
    print(results)


def main():
    try:
        run()
    except (AppError, ValidationError) as e:
        fatal(e)


if __name__ == "__main__":
    main()
