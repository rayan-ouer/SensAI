##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## spec
##

from pathlib import Path

import ollama

SPEC_TAGS = ("<current_document>", "</current_document>")


def load_spec(path: str) -> str:
    if Path(path).is_file():
        return Path(path).read_text(encoding="utf-8")
    return ""


def build_update_message(spec: str, user_input: str, reply: str) -> str:
    current = spec if spec else "(empty, this is the first exchange)"
    return f"""
<current_document>
{current}
</current_document>

<user_message>
{user_input}
</user_message>

<assistant_reply>
{reply}
</assistant_reply>

Return the updated document
"""


def strip_tags(text: str) -> str:
    for tag in SPEC_TAGS:
        text = text.replace(tag, "")
    return text


def strip_code_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.partition("\n")[2]
    if text.endswith("```"):
        text = text.removesuffix("```")
    return text.strip()


def update_spec(
    ollama_client_instance: ollama.Client,
    model: str,
    spec_prompt: str,
    spec: str,
    user_input: str,
    reply: str,
    think: str,
) -> str:
    spec_messages = [
        {"role": "system", "content": spec_prompt},
        {"role": "user", "content": build_update_message(spec, user_input, reply)},
    ]
    res = ollama_client_instance.chat(
        model=model,
        messages=spec_messages,
        stream=False,
        options={"temperature": 0},
        think=think,
    )
    new_spec = strip_code_fences(strip_tags(res.message.content))
    if not new_spec.startswith("#"):
        return spec
    return new_spec


def save_spec(path: str, content: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")


def build_system_prompt(system: str, profile_prompt: str, spec: str) -> str:
    if not spec:
        return f"""{system}
{profile_prompt}
"""
    return f"""{system}

{profile_prompt}

# Current project specification

{spec}
"""
