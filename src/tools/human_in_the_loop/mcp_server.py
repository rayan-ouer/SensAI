from collections.abc import Callable

from fastmcp import FastMCP

from core.tools import ToolHandler
from tools.mcp.adapter import MCPAdapter
from tools.mcp.client import MCPClient
from .utils import normalize_inputs, display_menu, prompt_for_answer

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


def register_human_in_the_loop_tools(
    manager: ToolHandler,
    answers: list[dict[str, str]],
    input_function: InputFunction = input,
) -> None:
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
    manager.register_many(adapter.list_tools())
