##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## chat
##

from agent.agent import Agent
from core.messages import AIMessage, HumanMessage
from interfaces.cli.conversation_handle import ConversationHandle
from interfaces.cli.cli_state import CliState
from interfaces.cli.setup import current_role
from tools.chat.chat_loop import read_user_input, refresh_spec
from tools.chat.commands import handle_command

def send_to_agent(
    agent: Agent, conversation: ConversationHandle, user_input: str
) -> AIMessage | None:
    conversation.add_human_message(HumanMessage(content=user_input))
 
    try:
      agent.invoke(conversation.get_used_history())
    except (LLMError, AgentIterationLimitError) as e:
      error(e)
      return None

def answer_user_message(agent: Agent, conversation: ConversationHandlestate: CliState, spec: str, user_input: str) -> str:
    agent.set_role(current_role(state, spec))
    state.display.reset()
    reply = send_to_agent(agent, conversation, user_input)
  
    if reply is None:
        return spec
    conversation.add_ai_message(reply)
    print()
    return refresh_spec(state.spec_llm, state.config, spec, user_input, reply.content)

def agent_loop(agent: Agent, conversation: ConversationHandle, state: CliState, spec: str):
    while True:
        user_input = read_user_input()
        if user_input is None or user_input == "/exit":
            break
        if user_input.startswith("/"):
            handle_command(state, user_input)
        elif user_input:
            spec = answer_user_message(agent, conversation, state, spec, user_input)
