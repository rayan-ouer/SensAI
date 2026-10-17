from core.conversation import IConversationService
from core.messages import AIMessage, HumanMessage, IMessage, SystemMessage, ToolMessage


class ConversationHandle:
    def __init__(self, service: IConversationService, conversation_id: str) -> None:
        self._service = service
        self.id = conversation_id

    def get_used_history(self) -> list[IMessage]:
        return self._service.get_used_history(self.id)

    def get_full_history(self) -> list[IMessage]:
        return self._service.get_full_history(self.id)

    def add_human_message(self, message: HumanMessage) -> IMessage:
        return self._service.add_human_message(self.id, message)

    def add_ai_message(self, message: AIMessage) -> IMessage:
        return self._service.add_ai_message(self.id, message)

    def add_tool_message(self, message: ToolMessage) -> IMessage:
        return self._service.add_tool_message(self.id, message)

    def add_system_message(self, message: SystemMessage) -> IMessage:
        return self._service.add_system_message(self.id, message)

    def clear(self) -> None:
        self._service.clear(self.id)
