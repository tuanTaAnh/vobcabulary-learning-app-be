from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.db.database import get_session
from app.models.models import StudyLog, Vocab

router = APIRouter(prefix="/stats", tags=["Stats"])


def default_day(date_str: str):
    return {
        "date": date_str,
        "words_added": 0,
        "flashcards_swiped": 0,
        "mcq_answered": 0,
        "mcq_correct": 0,
        "mcq_wrong": 0,
    }


def build_daily_stats(session: Session):
    vocabs = session.exec(select(Vocab)).all()
    logs = session.exec(select(StudyLog)).all()

    daily = {}

    for vocab in vocabs:
        date_str = vocab.created_at.date().isoformat()
        daily.setdefault(date_str, default_day(date_str))
        daily[date_str]["words_added"] += 1

    for log in logs:
        date_str = log.created_at.date().isoformat()
        daily.setdefault(date_str, default_day(date_str))

        if log.event_type in ["swipe", "flashcard_swipe"]:
            daily[date_str]["flashcards_swiped"] += 1

        if log.event_type == "mcq":
            daily[date_str]["mcq_answered"] += 1

            if log.correct is True:
                daily[date_str]["mcq_correct"] += 1
            elif log.correct is False:
                daily[date_str]["mcq_wrong"] += 1

    return sorted(daily.values(), key=lambda item: item["date"])


@router.get("")
def get_stats(session: Session = Depends(get_session)):
    return build_daily_stats(session)


@router.get("/daily")
def get_daily_stats(session: Session = Depends(get_session)):
    return build_daily_stats(session)


@router.get("/summary")
def get_stats_summary(session: Session = Depends(get_session)):
    vocabs = session.exec(select(Vocab)).all()
    logs = session.exec(select(StudyLog)).all()

    flashcard_logs = [
        log for log in logs if log.event_type in ["swipe", "flashcard_swipe"]
    ]

    mcq_logs = [
        log for log in logs if log.event_type == "mcq"
    ]

    correct_logs = [
        log for log in mcq_logs if log.correct is True
    ]

    wrong_logs = [
        log for log in mcq_logs if log.correct is False
    ]

    return {
        "total_words": len(vocabs),
        "total_flashcards": len(flashcard_logs),
        "total_mcq": len(mcq_logs),
        "total_correct": len(correct_logs),
        "total_wrong": len(wrong_logs),
    }