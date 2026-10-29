##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## spec
##

import json
from pathlib import Path

from core.messages import HumanMessage, SystemMessage
from llm.client import ILLMClient

SPEC_TITLE = "# Project specification"
SPEC_SECTIONS = (
    "Overview",
    "Goals",
    "Functional requirements",
    "Non-functional requirements",
    "Constraints",
    "Decisions",
    "Open questions",
)
EMPTY_SECTION = "_Nothing yet._"
EDIT_SCHEMA = {
    "type": "object",
    "properties": {
        "edits": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "section": {"type": "string", "enum": list(SPEC_SECTIONS)},
                    "content": {"type": "string"},
                },
                "required": ["section", "content"],
            },
        },
    },
    "required": ["edits"],
}


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

Return the edits of the sections that change, as JSON
"""


def parse_spec(spec: str) -> dict[str, str]:
    sections = {name: EMPTY_SECTION for name in SPEC_SECTIONS}
    for block in spec.split("\n## ")[1:]:
        name, _, content = block.partition("\n")
        if name.strip() in sections:
            sections[name.strip()] = content.strip() or EMPTY_SECTION
    return sections


def render_spec(sections: dict[str, str]) -> str:
    blocks = [SPEC_TITLE] + [f"## {name}\n{sections[name]}" for name in SPEC_SECTIONS]
    return "\n\n".join(blocks) + "\n"


def is_valid_edit(edit: object) -> bool:
    if not isinstance(edit, dict):
        return False
    return edit.get("section") in SPEC_SECTIONS and isinstance(edit.get("content"), str)


def read_edits(text: str) -> list[dict]:
    try:
        edits = json.loads(text).get("edits", [])
    except (json.JSONDecodeError, AttributeError):
        return []
    if not isinstance(edits, list):
        return []
    return [edit for edit in edits if is_valid_edit(edit)]


def apply_edits(spec: str, edits: list[dict]) -> str:
    sections = parse_spec(spec)
    for edit in edits:
        sections[edit["section"]] = edit["content"].strip() or EMPTY_SECTION
    return render_spec(sections)


def update_spec(
    llm_client_instance: ILLMClient,
    model: str,
    spec_prompt: str,
    spec: str,
    user_input: str,
    reply: str,
    spec_think: bool | None,
) -> str:
    spec_messages = [
        SystemMessage(content=spec_prompt),
        HumanMessage(content=build_update_message(spec, user_input, reply)),
    ]
    res = llm_client_instance.chat(model, spec_messages, [], EDIT_SCHEMA, think=spec_think)
    return apply_edits(spec, read_edits(res.content))


def save_spec(path: str, content: str) -> None:
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
