import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
    Enum as SQLEnum
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class MessageType(str, Enum):
    HUMAN = "human"
    AI = "ai"
    SYSTEM = "system"

class Base(DeclarativeBase):
    pass


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    title: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    active_message_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("messages.id", ondelete="SET NULL"),
        nullable=True,
    )

    active_message: Mapped["Message" | None] = relationship(
        "Message",
        foreign_keys=[active_message_id],
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="conversation",
        foreign_keys="Message.conversation_id",
        cascade="all, delete-orphan",
    )

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    conversation: Mapped[Conversation] = relationship(
        "Conversation",
        back_populates="messages",
        foreign_keys=[conversation_id],
    )

    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("messages.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    parent: Mapped["Message" | None] = relationship(
        "Message",
        back_populates="children",
        remote_side=[id],
    )

    role: Mapped[MessageType] = mapped_column(
        SQLEnum(MessageType),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    token_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    children: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="parent",
        cascade="all, delete-orphan",
    )
