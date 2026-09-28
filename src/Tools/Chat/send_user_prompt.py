import ollama

def send_user_prompt(messages: list, model: str) -> str:
    stream = ollama.chat(
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
