import argparse
import sys
import ollama

from src.Tools.Chat.send_user_prompt import send_user_prompt
from src.Tools.Chat.load_config import load_config

EXIT_ERR = 84

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    ret, config = load_config(parser)
    if ret != 0:
        sys.exit(ret)

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
        try:
            reply = send_user_prompt(messages, config["model"])
            print()
        except ollama.ResponseError as e:
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
            sys.exit(EXIT_ERR)

        messages.append({"role": "assistant", "content": reply})

    print("Bye bye")
