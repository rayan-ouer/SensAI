##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## main
##

from pydantic import ValidationError

from interfaces.cli.args import handle_args
from interfaces.cli.chat import agent_loop
from interfaces.cli.setup import (
    apply_agents_config,
    create_agent,
    create_cli_state,
    create_tools,
    current_role,
    load_agents_config,
    read_api_key,
)
from tools.chat.errors import AppError
from tools.chat.load_config import ConfigLoader
from tools.chat.module import fatal
from tools.spec.spec import load_spec


def run() -> None:
    args = handle_args()
    api_key = read_api_key()
    config = ConfigLoader(args.config).get_configs()
    state = create_cli_state(config, api_key)
    print(f"Starting {state.current_profile().name} with prompts {state.config.prompt_version}")
    spec = load_spec(state.config.spec_path)
    tools = create_tools(state)
    agents_config = load_agents_config(args.multi_agent, state.config.config_dir)
    apply_agents_config(state, agents_config)
    role = current_role(state, spec)
    agent = create_agent(state, tools, role, agents_config)
    agent_loop(agent, state, spec)


def main() -> None:
    try:
        run()
    except (AppError, ValidationError) as e:
        fatal(e)


if __name__ == "__main__":
    main()
