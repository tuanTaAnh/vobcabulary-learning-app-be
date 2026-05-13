from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class CollectionBase(SQLModel):
    name: str
    description: Optional[str] = None


class Collection(CollectionBase, table=True):
    __tablename__ = "collections"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    vocabs: list["Vocab"] = Relationship(back_populates="collection")


class CollectionCreate(CollectionBase):
    pass


class CollectionRead(CollectionBase):
    id: int
    created_at: datetime


class CollectionUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None


class VocabBase(SQLModel):
    german: str
    vietnamese: str
    examples: str = ""
    topic: Optional[str] = None
    collection_id: Optional[int] = Field(default=None, foreign_key="collections.id")
    swipe_count: int = 0
    is_starred: bool = False


class Vocab(VocabBase, table=True):
    __tablename__ = "vocab"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    collection: Optional[Collection] = Relationship(back_populates="vocabs")


class VocabCreate(VocabBase):
    collection_id: Optional[int] = None
    swipe_count: int = 0
    is_starred: bool = False


class VocabRead(VocabBase):
    id: int
    created_at: datetime
    collection_id: Optional[int] = None
    swipe_count: int = 0
    is_starred: bool = False


class VocabUpdate(SQLModel):
    german: Optional[str] = None
    vietnamese: Optional[str] = None
    examples: Optional[str] = None
    topic: Optional[str] = None
    collection_id: Optional[int] = None
    swipe_count: Optional[int] = None
    is_starred: Optional[bool] = None


class StudyLog(SQLModel, table=True):
    __tablename__ = "study_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    vocab_id: Optional[int] = Field(default=None, foreign_key="vocab.id")
    event_type: str
    correct: Optional[bool] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class StudyLogCreate(SQLModel):
    vocab_id: Optional[int] = None
    event_type: str
    correct: Optional[bool] = None


class StudyLogRead(StudyLogCreate):
    id: int
    created_at: datetime


class ChatSession(SQLModel, table=True):
    __tablename__ = "chat_sessions"

    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: str
    current_step: int = 0
    hint_level: int = 0
    finished: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    messages: list["ChatMessage"] = Relationship(back_populates="session")


class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: Optional[int] = Field(default=None, foreign_key="chat_sessions.id")
    role: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    session: Optional[ChatSession] = Relationship(back_populates="messages")