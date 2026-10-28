##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## args
##

import argparse


def handle_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SensAI command-line assistant")
    parser.add_argument(
        "-c",
        "--config",
        dest="config",
        type=str,
        required=True,
        help="YAML configuration file to use",
    )
    parser.add_argument(
        "-m",
        "--multi-agent",
        dest="multi_agent",
        type=str,
        required=False,
        help="Multi-agent YAML path",
    )
    return parser.parse_args()
