##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## module
##

import sys

EXIT_S = 0
EXIT_E = 84

def fatal(message: object):
    print(f"Error: {message}")
    sys.exit(EXIT_E)

def warning(message: object):
    print(f"Warning: {message}")
