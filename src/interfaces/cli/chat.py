##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## chat
##

from agent.agent import Agent, AgentIterationLimitError, AgentTurn
from core.messages import AIMessage, HumanMessage, ToolMessage
from interfaces.cli.cli_state import CliState
from interfaces.cli.conversation_handle import ConversationHandle
from interfaces.cli.setup import current_role
from llm.errors import LLMError
from tools.chat.chat_loop import read_user_input, refresh_spec
from tools.chat.commands import handle_command
from tools.chat.module import error


def send_to_agent(
        agent: Agent, conversation: ConversationHandle, user_input: str
) -> AIMessage | None:
    human_message: HumanMessage = HumanMessage(content=user_input)
    try:
        turn: AgentTurn = agent.invoke(conversation.get_used_history() + [human_message])
    except (LLMError, AgentIterationLimitError) as e:
        error(e)
        return None
    conversation.add_human_message(human_message)
    for message in turn.messages:
        if isinstance(message, AIMessage):
            conversation.add_ai_message(message)
        elif isinstance(message, ToolMessage):
            conversation.add_tool_message(message)
    return turn.reply

def answer_user_message(
        agent: Agent, state: CliState, spec: str, user_input: str
) -> tuple[str, str] | None:
    agent.set_role(current_role(state, spec))
    state.display.reset()
    state.human_answers.clear()
    reply = send_to_agent(agent, state.conversation, user_input)
    if reply is None:
        return None
    print()
    spec_user_input = user_input
    if state.human_answers:
        spec_user_input += "\n\nUser's answers to clarification questions:\n" + "\n".join(
            f"- {answer['question']} {answer['answer']}"
            for answer in state.human_answers
        )
    return spec_user_input, reply.content


def agent_loop(agent: Agent, state: CliState, spec: str):
    pending_spec_update: tuple[str, str] | None = None
    while True:
        user_input = read_user_input()
        if pending_spec_update is not None:
            spec_input, reply = pending_spec_update
            spec = refresh_spec(state.llm, state.config, spec, spec_input, reply)
            pending_spec_update = None
        if user_input is None or user_input == "/exit":
            break
        if user_input.startswith("/"):
            handle_command(state, user_input)
        elif user_input:
            pending_spec_update = answer_user_message(agent, state, spec, user_input)
