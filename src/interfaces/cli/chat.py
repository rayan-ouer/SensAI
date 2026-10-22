##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## chat
##

from agent.agent import Agent, AgentIterationLimitError
from core.messages import AIMessage, HumanMessage
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

def answer_user_message(agent: Agent, config: dict, spec: str, user_input: str) -> str:
    agent.set_role(current_role(config, spec))
    config["display"].reset()
    human_answers: list[dict[str, str]] = config.get("human_answers", [])
    human_answers.clear()
    reply = send_to_agent(agent, config["messages"], user_input)
    if reply is None:
        return spec
    print()
    spec_user_input = user_input
    if human_answers:
        spec_user_input += "\n\nUser's answers to clarification questions:\n" + "\n".join(
            f"- {answer['question']} {answer['answer']}" for answer in human_answers
        )
    return refresh_spec(
        config["spec_client"], config, spec, spec_user_input, reply.content
    )

def agent_loop(agent: Agent, config: dict, spec: str):
    config["messages"] = []
    while True:
        user_input = read_user_input()
        if user_input is None or user_input == "/exit":
            break
        if user_input.startswith("/"):
            handle_command(config, user_input)
        elif user_input:
            spec = answer_user_message(agent, config, spec, user_input)
