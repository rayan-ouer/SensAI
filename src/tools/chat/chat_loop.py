##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## chat_loop
##

import io
import sys
import ollama

from tools.chat.module import warning
from tools.spec.spec import save_spec, update_spec

_stdin_configured = False


def read_user_input() -> str | None:
    global _stdin_configured

    print("> ", end="", flush=True)
    try:
        if not _stdin_configured:
            if isinstance(sys.stdin, io.TextIOWrapper):
                sys.stdin.reconfigure(errors="replace")
            _stdin_configured = True
        return input()
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def refresh_spec(
    ollama_client_instance: ollama.Client,
    config: dict,
    spec: str,
    user_input: str,
    reply: str,
) -> str:
    try:
        new_spec = update_spec(
            ollama_client_instance,
            config["model"],
            config["spec_prompt"],
            spec,
            user_input,
            reply,
            config.get("spec_think"),
        )
        save_spec(config["spec_path"], new_spec)
        return new_spec
    except (ollama.ResponseError, ConnectionError, OSError) as e:
        warning(f"{config['spec_path']} not updated: {e}")
    except KeyboardInterrupt:
        print()
        warning(f"{config['spec_path']} update interrupted")
    return spec
