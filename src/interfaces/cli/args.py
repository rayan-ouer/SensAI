##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## args
##

import argparse

def handle_args():
    parser = argparse.ArgumentParser(description="SensAI command-line assistant")
    parser.add_argument(
        "-c", "--config", dest="config", type=str, required=True,
        help="YAML configuration file to use"
    )
    return parser.parse_args()
