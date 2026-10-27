##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## module
##

import sys
from typing import NoReturn

EXIT_S = 0
EXIT_E = 84

OLLAMA_LOCAL_HOST = "http://localhost:11434"
OLLAMA_CLOUD_HOST = "https://ollama.com"


def warning(message: object) -> None:
    print(f"Warning: {message}")


def error(message: object) -> None:
    print(f"Error: {message}")


def fatal(message: object) -> NoReturn:
    error(message)
    sys.exit(EXIT_E)
