##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## mcp_server
##

from collections.abc import Callable

from fastmcp import FastMCP

from core.tools import ITool
from tools.human_in_the_loop.utils import display_menu, normalize_inputs, prompt_for_answer
from tools.mcp.adapter import MCPAdapter
from tools.mcp.client import MCPClient

AnswerCallback = Callable[[str, str], None]
InputFunction = Callable[[str], str]


def create_human_in_the_loop_server(
    on_answer: AnswerCallback | None = None,
    input_function: InputFunction = input,
) -> FastMCP:
    mcp = FastMCP("sensai-human-in-the-loop")

    @mcp.tool
    def human_in_the_loop(question: str, options: list[str]) -> str:
        """Ask the user a closed question with an additional free-form choice.

        question: One concise question about a missing project specification.
        options: Two or more distinct proposed answers. A free-form "Other"
            option is added automatically.
        """
        question_text, choices = normalize_inputs(question, options)
        other_index = display_menu(question_text, choices)
        answer = prompt_for_answer(choices, other_index, input_function)

        if on_answer is not None:
            on_answer(question_text, answer)
        return answer

    return mcp


def create_human_in_the_loop_tools(
    answers: list[dict[str, str]],
    input_function: InputFunction = input,
) -> list[ITool]:
    def record_answer(question: str, answer: str) -> None:
        answers.append({"question": question, "answer": answer})

    adapter = MCPAdapter(
        MCPClient(
            create_human_in_the_loop_server(
                on_answer=record_answer,
                input_function=input_function,
            )
        )
    )
    return adapter.list_tools()
