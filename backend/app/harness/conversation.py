from abc import ABC

from sqlalchemy.orm import Session

from app.db.models import Conversation, Message, MessageType
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

    def get_conversation_by_id(id: str):
        pass

    def edit_message(message_id: str, _: IMessage):
        pass

    def clear():
        pass


class DatabaseConversation(IConversation):
    def __init__(self, session: Session):
        self._db: Session = Session

    def add_message(self, message: IMessage):
        pass        

    def add_ai_message(self, message: AIMessage):
        pass

    def add_human_message(self, message: HumanMessage):
        pass

    def get_used_history(self):
        pass

    def get_full_history(self):
        pass

    def get_conversation_by_id(id: str):
        pass

    def edit_message(self, message_id: str, new_message: IMessage):
        pass

    def clear(self):
        pass
