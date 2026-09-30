##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## spec
##

from pathlib import Path

import ollama

@staticmethod
def load_spec(path: str) -> str:
    if Path(path).is_file():
        return Path(path).read_text(encoding="utf-8")
    return ""

def update_spec(ollama_client_instance: ollama.Client, model: str, spec_prompt: str, spec: str, user_input: str, reply: str) -> str:
    user_message = f"""# Current WU.md
{spec if spec else "(empty, this is the first exchange)"}

# Last exchange
## User
{user_input}

## Wu
{reply}

Return the updated WU.md"""
    spec_messages = [{"role": "system", "content": spec_prompt}, {"role": "user", "content": user_message}]

    res =  ollama_client_instance.chat(
        model=model,
        messages=spec_messages,
        stream=False,
        options={"temperature": 0}
    )

    new_spec = res.message.content.strip()
    if new_spec.startswith("```"):
        new_spec = new_spec.partition("\n")[2]
    if new_spec.endswith("```"):
        new_spec = new_spec.removesuffix("```")
    new_spec = new_spec.strip()

    if new_spec == "":
        return spec
    return new_spec

def save_spec(path: str, content: str):
    Path(path).parent.mkdir(parents= True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")

def build_system_prompt(system: str, spec: str) -> str:
    if not spec:
        return system
    return f"""{system}

# Current project specification

{spec}
"""