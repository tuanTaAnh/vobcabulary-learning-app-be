import random
import re
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.database import get_session
from app.models.models import StudyLog, Vocab

router = APIRouter(prefix="/mcq", tags=["mcq"])


def get_example_lines(examples: str | None) -> list[str]:
    if not examples:
        return []

    return [
        line.strip()
        for line in examples.split("\n")
        if line.strip()
    ]


def get_maskable_example_lines(vocab: Vocab) -> list[str]:
    example_lines = get_example_lines(vocab.examples)

    if not example_lines:
        return []

    pattern = re.compile(re.escape(vocab.german), re.IGNORECASE)

    return [
        line
        for line in example_lines
        if pattern.search(line)
    ]


def mask_answer_in_sentence(sentence: str, answer: str) -> str:
    pattern = re.compile(re.escape(answer), re.IGNORECASE)
    return pattern.sub("_____", sentence, count=1)


@router.get("")
def get_mcq(
    collection_id: Optional[int] = None,
    session: Session = Depends(get_session),
):
    statement = select(Vocab)

    if collection_id is not None:
        statement = statement.where(Vocab.collection_id == collection_id)

    vocabs = session.exec(statement).all()

    eligible_vocabs = [
        vocab
        for vocab in vocabs
        if get_maskable_example_lines(vocab)
    ]

    if len(eligible_vocabs) < 4:
        raise HTTPException(
            status_code=400,
            detail=(
                "At least 4 words with usable example sentences are required "
                "to generate a quiz question."
            ),
        )

    answer = random.choice(eligible_vocabs)

    answer_examples = get_maskable_example_lines(answer)
    sentence = random.choice(answer_examples)
    masked_sentence = mask_answer_in_sentence(sentence, answer.german)

    distractors = [
        vocab
        for vocab in eligible_vocabs
        if vocab.id != answer.id
    ]

    options = random.sample(distractors, 3) + [answer]
    random.shuffle(options)

    return {
        "question": masked_sentence,
        "answer": answer.german,
        "answer_id": answer.id,
        "options": [vocab.german for vocab in options],
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