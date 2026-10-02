##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## send_user_prompt
##

import ollama

def print_part(text: str, header: str, show_header: bool):
    if show_header:
        print(header, end='', flush=True)
    print(text, end='', flush=True)

<<<<<<< HEAD
def print_chunk(message: ollama.Message, in_thinking: bool) -> bool:
    if message.thinking:
        print_part(message.thinking, 'Thinking:\n', not in_thinking)
        return True
    if message.content:
        print_part(message.content, '\n\nAnswer:\n', in_thinking)
        return False
    return in_thinking
=======
MODEL = "mistral"


def send_user_prompt(user_prompt: str, context: dict) -> str:
    stream = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        stream=True,
    )
>>>>>>> feat/architecture/messages_and_tools

def send_user_prompt(messages: list, model: str, ollama_client_instance: ollama.Client) -> str:
    stream = ollama_client_instance.chat(model=model, messages=messages, stream=True)
    in_thinking = False
<<<<<<< HEAD
    content = ''
    for chunk in stream:
        in_thinking = print_chunk(chunk.message, in_thinking)
        if chunk.message.content and not chunk.message.thinking:
=======
    content = ""
    thinking = ""
    for chunk in stream:
        if chunk.message.thinking:
            if not in_thinking:
                in_thinking = True
                print("Thinking:\n", end="", flush=True)
            print(chunk.message.thinking, end="", flush=True)
            thinking += chunk.message.thinking
        elif chunk.message.content:
            if in_thinking:
                in_thinking = False
                print("\n\nAnswer:\n", end="", flush=True)
            print(chunk.message.content, end="", flush=True)
>>>>>>> feat/architecture/messages_and_tools
            content += chunk.message.content
    return content
