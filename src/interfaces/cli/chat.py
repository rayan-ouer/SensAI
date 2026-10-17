##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## chat
##

from agent.agent import Agent, AgentIterationLimitError
from core.messages import AIMessage, HumanMessage
from interfaces.cli.session_data import Session
from interfaces.cli.setup import current_role
from llm.errors import LLMError
from tools.chat.chat_loop import read_user_input, refresh_spec
from tools.chat.commands import handle_command
from tools.chat.module import error


def send_to_agent(agent: Agent, messages: list, user_input: str) -> AIMessage | None:
    start = len(messages)
    messages.append(HumanMessage(content=user_input))
    try:
        return agent.invoke(messages)
    except (LLMError, AgentIterationLimitError) as e:
        error(e)
        del messages[start:]
        return None


def answer_user_message(agent: Agent, session: Session, spec: str, user_input: str) -> str:
    agent.set_role(current_role(session, spec))
    session.display.reset()
    reply = send_to_agent(agent, session.messages, user_input)
    if reply is None:
        return spec
    print()
    return refresh_spec(session.spec_client, session.config, spec, user_input, reply.content)


def agent_loop(agent: Agent, session: Session, spec: str):
    while True:
        user_input = read_user_input()
        if user_input is None or user_input == "/exit":
            break
        if user_input.startswith("/"):
            handle_command(session, user_input)
        elif user_input:
            spec = answer_user_message(agent, session, spec, user_input)
