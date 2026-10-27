##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## chat
##

from collections.abc import Callable, Iterator
from queue import Queue

from fastapi.datastructures import State

from agent.agent import Agent, AgentIterationLimitError, AgentTurn
from core.conversation import IConversationService
from core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from interfaces.api.schemas.output.conversation import StreamEvent
from llm.errors import LLMError
from tools.agent.profile_data import ProfileData
from tools.agent.profiles import build_profile_prompt
from tools.chat.chat_loop import refresh_spec
from tools.spec.spec import build_system_prompt, load_spec


def build_role(state: State, profile: ProfileData) -> SystemMessage:
    return SystemMessage(
        content=build_system_prompt(
            state.config.system_prompt,
            build_profile_prompt(profile),
            load_spec(state.config.spec_path),
        )
    )


def create_agent(
    state: State,
    on_chunk: Callable[[str, str], None],
    profile_key: str | None,
) -> Agent:
    profile = state.profiles[profile_key or state.config.default_profile]
    return Agent(
        name=profile.name,
        model=state.config.model,
        tools=[tool.name for tool in state.tools.list_tools()],
        role=build_role(state, profile),
        response_format=state.config.response_format,
        llm=state.llm,
        handler=state.tools,
        max_loops=state.config.max_loops,
        on_chunk=on_chunk,
    )


def save_turn(service: IConversationService, conversation_id: str, turn: AgentTurn) -> None:
    for message in turn.messages:
        if isinstance(message, AIMessage):
            service.add_ai_message(conversation_id, message)
        elif isinstance(message, ToolMessage):
            service.add_tool_message(conversation_id, message)


def send_spec_update(
    content: str,
    events: Queue,
    state: State,
    turn: AgentTurn,
) -> None:
    spec = load_spec(state.config.spec_path)
    new_spec = refresh_spec(state.llm, state.config, spec, content, turn.reply.content)
    events.put(StreamEvent(type="spec", text=new_spec))


def run_turn(
    agent: Agent,
    service: IConversationService,
    conversation_id: str,
    content: str,
    events: Queue,
    state: State,
) -> None:
    human = HumanMessage(content=content)
    try:
        turn = agent.invoke(service.get_used_history(conversation_id) + [human])
    except (LLMError, AgentIterationLimitError) as e:
        events.put(StreamEvent(type="error", message=str(e)))
        return
    service.add_human_message(conversation_id, human)
    save_turn(service, conversation_id, turn)
    events.put(StreamEvent(type="done"))
    send_spec_update(content, events, state, turn)


def stream_events(events: Queue) -> Iterator[str]:
    while True:
        event: StreamEvent = events.get()
        yield event.model_dump_json(exclude_none=True) + "\n"
        if event.type == "error" or event.type == "spec":
            return
