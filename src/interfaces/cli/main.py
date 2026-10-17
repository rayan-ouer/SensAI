##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## main
##

from pydantic import ValidationError

from interfaces.cli.args import handle_args
from interfaces.cli.chat import agent_loop
from interfaces.cli.display import ChunkDisplay
from interfaces.cli.setup import create_agent, current_role, read_api_key
from tools.agent.profiles import init_profiles
from tools.chat.create_client import create_ollama_client
from tools.chat.errors import AppError
from tools.chat.load_config import load_config_file
from tools.chat.module import fatal
from tools.spec.spec import load_spec

def run():
    args = handle_args()
    api_key = read_api_key()
    config = load_config_file(args.config)
    init_profiles(config)
    print(f"Starting {config['profiles'][config['active_profile']]['name']}")
    spec = load_spec(config["spec_path"])
    config["spec_client"] = create_ollama_client(config["model"], api_key)
    config["display"] = ChunkDisplay()
    agent = create_agent(config, api_key, current_role(config, spec))
    agent_loop(agent, config, spec)
    print("Bye bye")

def main():
    try:
        run()
    except (AppError, ValidationError) as e:
        fatal(e)

if __name__ == "__main__":
    main()
