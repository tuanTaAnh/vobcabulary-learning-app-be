from datetime import datetime
from typing import Optional, List

from sqlmodel import SQLModel


class VocabCreate(SQLModel):
    german: str
    vietnamese: str
    examples: str = ""
    topic: Optional[str] = None


class VocabRead(SQLModel):
    id: int
    german: str
    vietnamese: str
    examples: str
    topic: Optional[str]
    created_at: datetime
    swipe_count: int


class VocabUpdate(SQLModel):
    german: Optional[str] = None
    vietnamese: Optional[str] = None
    examples: Optional[str] = None
    topic: Optional[str] = None


class GenerateExamplesRequest(SQLModel):
    german: str
    vietnamese: str
    topic: Optional[str] = None
    level: str = "A2"


class GenerateExamplesResponse(SQLModel):
    examples: List[str]


class MCQQuestion(SQLModel):
    vocab_id: int
    sentence: str
    options: List[str]
    answer: str
    explanation: Optional[str] = None


class MCQSubmit(SQLModel):
    vocab_id: int
    selected_answer: str
    correct_answer: str


class DailyStats(SQLModel):
    date: str
    words_added: int
    swipes: int
    mcq_total: int
    mcq_correct: int
    mcq_wrong: int


class ChatTopic(SQLModel):
    id: str
    title: str
    description: str
    image_url: str
    background_url: str


class StartChatRequest(SQLModel):
    topic_id: str


class StartChatResponse(SQLModel):
    session_id: int
    topic: ChatTopic
    ai_message: str
    masked_answer: str
    full_answer: str
    hint_level: int


class ChatAnswerRequest(SQLModel):
    session_id: int
    user_answer: str


class ChatAnswerResponse(SQLModel):
    is_correct_like: bool
    feedback: str
    ai_message: str
    masked_answer: str
    full_answer: str
    hint_level: int
    finished: bool


class HintRequest(SQLModel):
    session_id: int
    hint_level: int


class HintResponse(SQLModel):
    masked_answer: str
    hint_level: int
