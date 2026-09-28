from abc import ABC

from .messages import AIMessage, HumanMessage, IMessage


class IConversation(ABC):
    def add_message(message: IMessage):
        pass

    def add_ai_message(message: AIMessage):
        pass

    def add_human_message(message: HumanMessage):
        pass

    def get_used_history():
        pass

    def get_full_history():
        pass

    def clear():
        pass


class DatabaseConversation(IConversation):
    pass
