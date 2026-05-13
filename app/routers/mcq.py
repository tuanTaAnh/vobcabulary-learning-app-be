import random
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.database import get_session
from app.models.models import StudyLog, Vocab

router = APIRouter(prefix="/mcq", tags=["mcq"])


@router.get("")
def get_mcq(
    collection_id: Optional[int] = None,
    session: Session = Depends(get_session),
):
    statement = select(Vocab)

    if collection_id is not None:
        statement = statement.where(Vocab.collection_id == collection_id)

    vocabs = session.exec(statement).all()

    if len(vocabs) < 4:
        raise HTTPException(
            status_code=400,
            detail="At least 4 words are required to generate a quiz question.",
        )

    answer = random.choice(vocabs)

    example_lines = [
        line.strip()
        for line in answer.examples.split("\n")
        if line.strip()
    ]

    if example_lines:
        sentence = random.choice(example_lines)
    else:
        sentence = f"Ich benutze das Wort {answer.german} in einem einfachen Satz."

    masked_sentence = sentence.replace(answer.german, "_____")

    if masked_sentence == sentence:
        masked_sentence = f"Ich benutze das Wort _____ in einem einfachen Satz."

    distractors = [v for v in vocabs if v.id != answer.id]
    options = random.sample(distractors, 3) + [answer]
    random.shuffle(options)

    return {
        "question": masked_sentence,
        "answer": answer.german,
        "answer_id": answer.id,
        "options": [v.german for v in options],
    }


@router.post("/record")
def record_mcq_result(
    vocab_id: Optional[int] = None,
    correct: bool = False,
    session: Session = Depends(get_session),
):
    log = StudyLog(
        vocab_id=vocab_id,
        event_type="mcq",
        correct=correct,
    )

    session.add(log)
    session.commit()

    return {"recorded": True}