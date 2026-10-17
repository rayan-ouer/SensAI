##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## main
##

from pydantic import ValidationError

from interfaces.cli.args import handle_args
from interfaces.cli.chat import agent_loop
from interfaces.cli.setup import create_agent, create_session, current_role, read_api_key
from tools.chat.errors import AppError
from tools.chat.load_config import ConfigLoader
from tools.chat.module import fatal
from tools.spec.spec import load_spec


def run():
    args = handle_args()
    api_key = read_api_key()
    config = ConfigLoader(args.config).get_configs()
    session = create_session(config, api_key)
    print(f"Starting {session.current_profile().name}")
    spec = load_spec(session.config.spec_path)
    agent = create_agent(session, api_key, current_role(session, spec))
    agent_loop(agent, session, spec)
    print("Bye bye")


def main():
    try:
        run()
    except (AppError, ValidationError) as e:
        fatal(e)


if __name__ == "__main__":
    main()
