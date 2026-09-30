##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## main
##

import argparse
import sys
import ollama
import os
import dotenv

from src.Tools.Chat.module import EXIT_S, EXIT_E

from src.Tools.Chat.send_user_prompt import send_user_prompt
from src.Tools.Chat.load_config import load_config
from src.Tools.Chat.create_client import ollama_client
from src.Tools.Chat.model_list import get_model_list
from src.Tools.Wu.spec import load_spec, update_spec, save_spec, build_system_prompt

if __name__ == '__main__':
    dotenv.load_dotenv()
    ollama_api_key = os.environ.get("OLLAMA_API_KEY")

    parser = argparse.ArgumentParser()
    ret, config = load_config(parser)
    if ret != EXIT_S:
        sys.exit(ret)

    spec = load_spec(config["spec_path"])

    ollama_client_instance = ollama_client(config, ollama_api_key)

    messages = [{"role": "system", "content": config["system"]}]
    while True:
        print("> ", end="", flush=True)

        try:
            user_input = input()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if len(user_input) == 0: continue
        if user_input == "exit": break

        messages.append({"role": "user", "content": user_input})
        messages[0]["content"] = build_system_prompt(config["system"], spec)

        try:
            reply = send_user_prompt(messages, config["model"], ollama_client_instance)
            print()
        except ollama.ResponseError as e:
            if e.status_code == 401:
                print("Error: API key expired or invalid")
                sys.exit(EXIT_E)
            print(f"Error: {e.error}")
            messages.pop()
            continue
        except KeyboardInterrupt:
            print()
            print("Interrupted by user")
            messages.pop()
            continue
        except ConnectionError as e:
            print(f"Error: {e}")
            sys.exit(EXIT_E)

        messages.append({"role": "assistant", "content": reply})
        try:
            new_spec = update_spec(ollama_client_instance, config["model"], config["spec_prompt"], spec, user_input, reply)
            save_spec(config["spec_path"], new_spec)
            spec = new_spec
        except (ollama.ResponseError, ConnectionError, OSError) as e:
            print(f"Warning: WU.md not updated: {e}")
        except KeyboardInterrupt:
            print()
            print("Warning: WU.md update interrupted")

    print()
    print("Bye bye")
