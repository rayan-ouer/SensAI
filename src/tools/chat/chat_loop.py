##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## chat_loop
##

import io
import sys

from llm.client import ILLMClient
from llm.errors import LLMError
from tools.chat.config_data import ConfigData
from tools.chat.module import warning
from tools.spec.spec import save_spec, update_spec


def configure_stdin() -> None:
    if isinstance(sys.stdin, io.TextIOWrapper):
        sys.stdin.reconfigure(errors="replace")


def read_user_input() -> str | None:
    print("> ", end="", flush=True)
    try:
        return input()
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def refresh_spec(
    llm_client_instance: ILLMClient,
    config: ConfigData,
    spec: str,
    user_input: str,
    reply: str,
) -> str:
    try:
        args = (config.model, config.spec_prompt, spec, user_input, reply, config.spec_think)
        new_spec = update_spec(llm_client_instance, *args)
        save_spec(config.spec_path, new_spec)
        return new_spec
    except (LLMError, OSError) as e:
        warning(f"{config.spec_path} not updated: {e}")
    except KeyboardInterrupt:
        print()
        warning(f"{config.spec_path} update interrupted")
    return spec
