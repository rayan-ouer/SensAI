##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## conversation
##

from abc import ABC, abstractmethod

from .messages import AIMessage, HumanMessage, IMessage, SystemMessage, ToolMessage


class ConversationError(Exception):
    """Base exception for conversation-related errors."""


class ConversationNotFoundError(Exception):
    """Exception class when a conversation is not found."""

    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id
        super().__init__(f"Conversation {conversation_id} not found.")


class MessageError(Exception):
    """Base exception for message-related errors."""


class MessageNotFoundError(Exception):
    """Exception class when a conversation is not found."""

    def __init__(self, message_id: str):
        self.message_id = message_id
        super().__init__(f"Message {message_id} not found.")


class IConversationService(ABC):
    @abstractmethod
    def create_conversation(
        self,
        user_id: str,
        system_prompt: str | None = None,
    ) -> str:
        pass

    @abstractmethod
    def get_conversation_by_id_or_none(self, conversation_id: str):
        pass

    @abstractmethod
    def get_message_by_id_or_none(self, conversation_id: str, message_id: str):
        pass

    @abstractmethod
    def get_conversation_by_id(self, conversation_id: str):
        pass

    @abstractmethod
    def get_message_by_id(self, conversation_id: str, message_id: str):
        pass

    @abstractmethod
    def get_active_message(self, conversation_id: str):
        pass

    @abstractmethod
    def get_full_history(self, conversation_id: str) -> list[IMessage]:
        pass

    @abstractmethod
    def get_used_history(self, conversation_id: str) -> list[IMessage]:
        pass

    @abstractmethod
    def add_message(self, conversation_id: str, message: IMessage):
        pass

    @abstractmethod
    def add_ai_message(self, conversation_id: str, message: AIMessage):
        pass

    @abstractmethod
    def add_tool_message(self, conversation_id: str, message: ToolMessage):
        pass

    @abstractmethod
    def add_human_message(self, conversation_id: str, message: HumanMessage):
        pass

    @abstractmethod
    def add_system_message(self, conversation_id: str, message: SystemMessage):
        pass

    @abstractmethod
    def edit_message(self, conversation_id: str, message_id: str, message: IMessage):
        pass

    @abstractmethod
    def clear(self, conversation_id: str):
        pass
