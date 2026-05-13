from datetime import datetime, time
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.database import get_session
from app.models.models import StudyLog, Vocab, VocabCreate, VocabRead, VocabUpdate
router = APIRouter(prefix="/vocab", tags=["vocab"])


@router.get("", response_model=list[VocabRead])
def list_vocabs(
    collection_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    topic: Optional[str] = None,
    session: Session = Depends(get_session),
):
    statement = select(Vocab)

    if collection_id is not None:
        statement = statement.where(Vocab.collection_id == collection_id)

    if topic:
        statement = statement.where(Vocab.topic.contains(topic))

    if start_date:
        start_dt = datetime.combine(datetime.fromisoformat(start_date).date(), time.min)
        statement = statement.where(Vocab.created_at >= start_dt)

    if end_date:
        end_dt = datetime.combine(datetime.fromisoformat(end_date).date(), time.max)
        statement = statement.where(Vocab.created_at <= end_dt)

    statement = statement.order_by(Vocab.created_at.desc())

    return session.exec(statement).all()


@router.post("", response_model=VocabRead)
def create_vocab(
    vocab_create: VocabCreate,
    session: Session = Depends(get_session),
):
    vocab = Vocab.model_validate(vocab_create)

    session.add(vocab)
    session.commit()
    session.refresh(vocab)

    return vocab


@router.put("/{vocab_id}", response_model=VocabRead)
def update_vocab(
    vocab_id: int,
    vocab_update: VocabUpdate,
    session: Session = Depends(get_session),
):
    vocab = session.get(Vocab, vocab_id)

    if not vocab:
        raise HTTPException(status_code=404, detail="Vocab not found")

    update_data = vocab_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(vocab, key, value)

    session.add(vocab)
    session.commit()
    session.refresh(vocab)

    return vocab


@router.delete("/{vocab_id}")
def delete_vocab(
    vocab_id: int,
    session: Session = Depends(get_session),
):
    vocab = session.get(Vocab, vocab_id)

    if not vocab:
        raise HTTPException(status_code=404, detail="Vocab not found")

    session.delete(vocab)
    session.commit()

    return {"deleted": True}


@router.post("/{vocab_id}/swipe")
def record_vocab_swipe(
    vocab_id: int,
    session: Session = Depends(get_session),
):
    vocab = session.get(Vocab, vocab_id)

    if not vocab:
        raise HTTPException(status_code=404, detail="Vocab not found")

    log = StudyLog(
        vocab_id=vocab_id,
        event_type="flashcard_swipe",
        correct=None,
    )

    session.add(log)
    session.commit()

    return {"recorded": True}