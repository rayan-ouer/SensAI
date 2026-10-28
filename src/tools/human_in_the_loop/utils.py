##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## utils
##

from collections.abc import Callable


def normalize_inputs(question: str, options: list[str]) -> tuple[str, list[str]]:
    question_text = question.strip()
    choices = [option.strip() for option in options if option.strip()]

    if not question_text:
        raise ValueError("question is required")
    if len(choices) < 2:
        raise ValueError("at least two non-empty options are required")
    if len(set(choices)) != len(choices):
        raise ValueError("options must be distinct")

    return question_text, choices


def display_menu(question_text: str, choices: list[str]) -> int:
    print(question_text)
    for index, choice in enumerate(choices, start=1):
        print(f"{index}. {choice}")
    other_index = len(choices) + 1
    print(f"{other_index}. Other free-form answer")
    return other_index


def parse_selection(raw: str) -> int | None:
    try:
        return int(raw.strip())
    except ValueError:
        return None


def ask_free_form(input_function) -> str | None:
    answer = input_function("Your answer: ").strip()
    if answer:
        return answer
    print("Please provide a non-empty answer.")
    return None


def prompt_for_answer(choices: list[str], other_index: int, input_function) -> str:
    while True:
        selection = parse_selection(input_function("Choose an option number: "))

        if selection is None:
            print("Enter one of the listed option numbers.")
        elif 1 <= selection <= len(choices):
            return choices[selection - 1]
        elif selection == other_index:
            answer = ask_free_form(input_function)
            if answer is not None:
                return answer
        else:
            print("Enter one of the listed option numbers.")


def ask_in_terminal(question_text: str, choices: list[str], input_function: Callable[[str], str]) -> str:
    other_index = display_menu(question_text, choices)
    return prompt_for_answer(choices, other_index, input_function)
