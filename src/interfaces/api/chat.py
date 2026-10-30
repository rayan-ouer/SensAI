##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## chat
##

from collections.abc import Iterator
from functools import partial
from queue import Queue
from time import perf_counter

from fastapi.datastructures import State

from agent.agent import Agent, AgentTurn
from core.conversation import IConversationService
from core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from core.tools import ToolHandler
from interfaces.api.schemas.output.conversation import StreamEvent
from tools.agent.profile_data import ProfileData
from tools.agent.profiles import build_profile_prompt
from tools.chat.chat_loop import refresh_spec
from tools.human_in_the_loop.mcp_server import create_human_in_the_loop_tools
from tools.spec.spec import build_system_prompt, load_spec


def ask_in_stream(events: Queue, shown: str, question: str, options: list[str]) -> str:
    events.put(StreamEvent(type="question", text=question, options=options))
    return shown


def build_tools(state: State, events: Queue) -> ToolHandler:
    tool_handler = ToolHandler()
    tool_handler.register_many(state.tools.list_tools())
    ask = partial(ask_in_stream, events, state.config.question_prompt)
    tool_handler.register_many(create_human_in_the_loop_tools([], ask=ask))
    return tool_handler


def build_role(state: State, profile: ProfileData) -> SystemMessage:
    return SystemMessage(
        content=build_system_prompt(
            state.config.system_prompt,
            build_profile_prompt(profile),
            load_spec(state.config.spec_path),
        )
    )


def create_agent(state: State, events: Queue, profile_key: str | None, model: str | None) -> Agent:
    handler = build_tools(state, events)
    profile = state.profiles[profile_key or state.config.default_profile]
    return Agent(
        name=profile.name, model=model or state.config.model, tools=[tool.name for tool in handler.list_tools()],
        role=build_role(state, profile), response_format=state.config.response_format, llm=state.llm,
        handler=handler, max_loops=state.config.max_loops, think=state.config.think,
        on_chunk=lambda kind, text: events.put(StreamEvent(type=kind, text=text)),
        on_tool_call=state.monitor.record_tool,
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
) -> AgentTurn:
    human = HumanMessage(content=content)
    turn = agent.invoke(service.get_used_history(conversation_id) + [human])
    service.add_human_message(conversation_id, human)
    save_turn(service, conversation_id, turn)
    if turn.prompt_tokens is not None or turn.completion_tokens is not None:
        prompt_tokens = turn.prompt_tokens or 0
        completion_tokens = turn.completion_tokens or 0
        events.put(
            StreamEvent(
                type="usage",
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens,
            )
        )
    events.put(StreamEvent(type="done"))
    send_spec_update(content, events, state, turn)
    return turn


def run_turn_safely(
    agent: Agent,
    service: IConversationService,
    conversation_id: str,
    content: str,
    events: Queue,
    state: State,
) -> None:
    started = perf_counter()
    turn: AgentTurn | None = None
    error: Exception | None = None
    with state.monitor.bind(conversation_id, agent.name, state.config.model):
        try:
            turn = run_turn(agent, service, conversation_id, content, events, state)
        except Exception as e:
            error = e
            events.put(StreamEvent(type="error", message=str(e)))
        finally:
            state.monitor.record(
                "interaction",
                prompt=content,
                response=turn.reply.content if turn else None,
                latency_ms=(perf_counter() - started) * 1000,
                prompt_tokens=turn.prompt_tokens if turn else None,
                completion_tokens=turn.completion_tokens if turn else None,
                success=error is None and turn is not None,
                error=str(error) if error else None,
            )


def stream_events(events: Queue) -> Iterator[str]:
    while True:
        event: StreamEvent = events.get()
        yield event.model_dump_json(exclude_none=True) + "\n"
        if event.type == "error" or event.type == "spec":
            return
