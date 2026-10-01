from enum import Enum

class MessageType(str, Enum):
    HUMAN = "human"
    AI = "ai"
    SYSTEM = "system"
    TOOL = "tool"

class ToolStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"