from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Any, Callable


@dataclass_json
@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


class Tool:
    name: str
    description: str

    function: Callable[...] = None
