##
## EPITECH PROJECT, 2026
## G-AIA-500-PAR-5-1-sensai-1
## File description:
## send_user_prompt
##

import ollama

def send_user_prompt(messages: list, model: str, ollama_client_instance: ollama.Client) -> str:
    stream = ollama_client_instance.chat(
        model=model,
        messages=messages,
        stream=True,
    )

    in_thinking = False
    content = ''
    thinking = ''
    for chunk in stream:
        if chunk.message.thinking:
            if not in_thinking:
                in_thinking = True
                print('Thinking:\n', end='', flush=True)
            print(chunk.message.thinking, end='', flush=True)
            thinking += chunk.message.thinking
        elif chunk.message.content:
            if in_thinking:
                in_thinking = False
                print('\n\nAnswer:\n', end='', flush=True)
            print(chunk.message.content, end='', flush=True)
            content += chunk.message.content
    return content
