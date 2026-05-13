from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from app.db.database import get_session
from app.services.chat_service import (
    answer_session,
    get_hint,
    get_topics,
    start_session,
)


router = APIRouter(prefix="/chat", tags=["Chat Game"])


class ChatTopic(BaseModel):
    id: str
    title: str
    description: str
    image: str


class ChatMessageRead(BaseModel):
    role: str
    content: str


class StartChatRequest(BaseModel):
    topic_id: str


class StartChatResponse(BaseModel):
    session_id: int
    topic_id: str
    topic_title: str
    topic_description: str
    topic_image: str
    current_step: int
    total_steps: int
    question: str
    masked_answer: str
    full_answer: str
    hint_level: int
    finished: bool
    messages: list[ChatMessageRead]


class HintRequest(BaseModel):
    session_id: int
    hint_level: Optional[int] = None


class HintResponse(BaseModel):
    session_id: int
    hint_level: int
    masked_answer: str
    full_answer: str


class ChatAnswerRequest(BaseModel):
    session_id: int
    answer: str


class ChatAnswerResponse(StartChatResponse):
    is_correct: bool
    should_advance: bool
    score: int
    feedback: str
    corrected_answer: str


@router.get("/topics", response_model=list[ChatTopic])
def list_topics():
    return get_topics()


@router.post("/start", response_model=StartChatResponse)
def start_chat(
    payload: StartChatRequest,
    session: Session = Depends(get_session),
):
    try:
        return start_session(session, payload.topic_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post("/hint", response_model=HintResponse)
def request_hint(
    payload: HintRequest,
    session: Session = Depends(get_session),
):
    try:
        return get_hint(session, payload.session_id, payload.hint_level)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post("/answer", response_model=ChatAnswerResponse)
def answer_chat(
    payload: ChatAnswerRequest,
    session: Session = Depends(get_session),
):
    try:
        return answer_session(session, payload.session_id, payload.answer)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))