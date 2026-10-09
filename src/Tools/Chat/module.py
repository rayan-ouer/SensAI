##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## module
##

import sys

EXIT_S = 0
EXIT_E = 84

def warning(message: object):
    print(f"Warning: {message}")

def error(message: object):
    print(f"Error: {message}")

def fatal(message: object):
    error(message)
    sys.exit(EXIT_E)

