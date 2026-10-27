from typing import Annotated

from fastapi import Depends
from fastapi.params import State

from core.conversation import IConversationService
from memory.conversation.factory import ConversationServiceFactory, ConversationStorage

ConversationStorageDep = Annotated[
    ConversationStorage, Depends(lambda: State().storage)
]
ConversationDep = Annotated[
    IConversationService,
    Depends(ConversationServiceFactory().create(ConversationStorageDep)),
]
