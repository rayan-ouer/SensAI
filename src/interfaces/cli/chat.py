##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## chat
##

from agent.agent import Agent
from core.messages import AIMessage, HumanMessage
from interfaces.cli.conversation_handle import ConversationHandle
from interfaces.cli.setup import current_role
from tools.chat.chat_loop import read_user_input, refresh_spec
from tools.chat.commands import handle_command


def send_to_agent(
    agent: Agent, conversation: ConversationHandle, user_input: str
) -> AIMessage | None:
    conversation.add_human_message(HumanMessage(content=user_input))
    return agent.invoke(conversation.get_used_history())


def answer_user_message(
    agent: Agent,
    conversation: ConversationHandle,
    config: dict,
    spec: str,
    user_input: str,
) -> str:
    agent.set_role(current_role(config, spec))
    config["display"].reset()
    reply = send_to_agent(agent, conversation, user_input)
    if reply:
        conversation.add_ai_message(reply)
    print(reply.content)
    return refresh_spec(config["spec_client"], config, spec, user_input, reply.content)


def agent_loop(agent: Agent, conversation: ConversationHandle, config: dict, spec: str):
    while True:
        user_input = read_user_input()
        if user_input is None or user_input == "/exit":
            break
        if user_input.startswith("/"):
            handle_command(config, user_input)
        elif user_input:
            spec = answer_user_message(agent, conversation, config, spec, user_input)
