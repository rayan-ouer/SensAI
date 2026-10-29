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


def warning(message: object) -> None:
    print(f"Warning: {message}")


def error(message: object) -> None:
    print(f"Error: {message}")


def fatal(message: object) -> NoReturn:
    error(message)
    sys.exit(EXIT_E)
