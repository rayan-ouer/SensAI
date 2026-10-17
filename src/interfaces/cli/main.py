##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## main
##

from pydantic import ValidationError

from interfaces.cli.args import handle_args
from interfaces.cli.chat import agent_loop
from interfaces.cli.conversation_handle import ConversationHandle
from interfaces.cli.display import ChunkDisplay
from interfaces.cli.setup import create_agent, read_api_key
from llm.client import ILLMClient
from llm.ollama import OllamaClient
from memory.conversation.factory import ConversationServiceFactory, ConversationStorage
from tools.agent.profiles import init_profiles
from interfaces.cli.setup import create_agent, create_cli_state, current_role, read_api_key
from tools.chat.errors import AppError
from tools.chat.load_config import ConfigLoader
from tools.chat.module import fatal
from tools.spec.spec import load_spec
from core.tools import ITool
from tools.mcp.adapter import MCPAdapter
from tools.mcp.client import MCPClient
from tools.search.web import create_search_server


def init_conversation(config: dict) -> ConversationHandle:
    service = ConversationServiceFactory().create(ConversationStorage.MEMORY)
    conversation_id = service.create_conversation(
        user_id="local",
        system_prompt=config["system_prompt"],
    )
    return ConversationHandle(service, conversation_id)


def run():
    args = handle_args()
    api_key = read_api_key()
    config = ConfigLoader(args.config).get_configs()
    state = create_cli_state(config, api_key)
    conversation = init_conversation(config)
    mcp_tools = MCPAdapter(MCPClient(create_search_server()))
    tools: list[ITool] = list[ITool](mcp_tools.list_tools())
    print(f"Starting {state.current_profile().name}")
    spec = load_spec(state.config.spec_path)
    agent = create_agent(state, tools, current_role(state, spec))
    agent_loop(agent, conversation, state, spec)
    print("Bye bye")


def main():
    try:
        run()
    except (AppError, ValidationError) as e:
        fatal(e)


if __name__ == "__main__":
    main()
