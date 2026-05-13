from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from sqlmodel import Session, select

from app.models.models import ChatMessage, ChatSession


SceneStep = dict[str, Any]
SceneTopic = dict[str, Any]


TOPICS: list[SceneTopic] = [
    {
        "id": "farmers_market",
        "title": "At the Farmers' Market",
        "description": "Practice buying fruit, vegetables, quantities, and payment.",
        "image": "/images/scenes/farmers-market-cartoon.png",
        "steps": [
            {
                "question": "Guten Morgen! Was möchten Sie kaufen?",
                "target_answer": "Ich möchte zwei Kilo Äpfel kaufen.",
                "required": [["äpfel", "aepfel", "apfel"], ["zwei", "2"], ["kilo"]],
                "forbidden": ["supermarkt", "bahnhof", "bäckerei", "baeckerei"],
            },
            {
                "question": "Möchten Sie sonst noch etwas?",
                "target_answer": "Ja, bitte ein Kilo Tomaten.",
                "required": [["tomaten", "tomate"], ["ein kilo", "1 kilo", "kilo"]],
                "forbidden": ["ticket", "fahrkarte", "brot"],
            },
            {
                "question": "Brauchen Sie eine Tüte?",
                "target_answer": "Ja, bitte eine kleine Tüte.",
                "required": [["tüte", "tuete", "beutel"]],
                "forbidden": ["nein"],
            },
            {
                "question": "Das macht sechs Euro fünfzig. Zahlen Sie bar oder mit Karte?",
                "target_answer": "Ich zahle mit Karte.",
                "required": [["karte", "mit karte"]],
                "forbidden": ["bar"],
            },
            {
                "question": "Möchten Sie den Kassenbon?",
                "target_answer": "Nein, danke.",
                "required": [["nein", "no"], ["danke"]],
                "forbidden": [],
            },
            {
                "question": "Vielen Dank. Einen schönen Tag noch!",
                "target_answer": "Danke, Ihnen auch.",
                "required": [["danke"], ["auch"]],
                "forbidden": [],
            },
        ],
    },
    {
        "id": "train_station",
        "title": "Finding the Train Station",
        "description": "Practice asking for directions and buying a ticket.",
        "image": "/images/scenes/train-station-cartoon.png",
        "steps": [
            {
                "question": "Entschuldigung, wohin möchten Sie fahren?",
                "target_answer": "Ich möchte zum Hauptbahnhof fahren.",
                "required": [["hauptbahnhof", "bahnhof"], ["fahren", "gehen", "möchte", "moechte"]],
                "forbidden": ["supermarkt", "bäckerei", "baeckerei", "markt"],
            },
            {
                "question": "Brauchen Sie eine einfache Fahrt oder Hin und zurück?",
                "target_answer": "Eine einfache Fahrt, bitte.",
                "required": [["einfache fahrt", "einfach"], ["bitte"]],
                "forbidden": ["hin und zurück", "hin und zurueck"],
            },
            {
                "question": "Für welche Zone brauchen Sie die Fahrkarte?",
                "target_answer": "Ich brauche eine Fahrkarte für Zone AB.",
                "required": [["fahrkarte", "ticket"], ["zone ab", "ab"]],
                "forbidden": ["brot", "äpfel", "aepfel", "supermarkt"],
            },
            {
                "question": "Möchten Sie mit Karte zahlen?",
                "target_answer": "Ja, ich zahle mit Karte.",
                "required": [["ja"], ["karte"]],
                "forbidden": ["bar"],
            },
            {
                "question": "Der Zug fährt von Gleis zwei. Haben Sie noch eine Frage?",
                "target_answer": "Nein, danke. Das ist alles.",
                "required": [["nein"], ["danke"]],
                "forbidden": [],
            },
            {
                "question": "Alles klar. Gute Fahrt!",
                "target_answer": "Danke, auf Wiedersehen.",
                "required": [["danke"], ["wiedersehen", "tschüss", "tschuess"]],
                "forbidden": [],
            },
        ],
    },
    {
        "id": "bakery",
        "title": "At the Bakery Café",
        "description": "Practice ordering bread, coffee, snacks, and takeaway.",
        "image": "/images/scenes/bakery-cartoon.png",
        "steps": [
            {
                "question": "Guten Morgen! Was darf es sein?",
                "target_answer": "Ich hätte gern ein Brötchen und einen Kaffee.",
                "required": [["brötchen", "broetchen"], ["kaffee"]],
                "forbidden": ["fahrkarte", "bahnhof", "tomaten"],
            },
            {
                "question": "Möchten Sie den Kaffee groß oder klein?",
                "target_answer": "Einen kleinen Kaffee, bitte.",
                "required": [["klein", "kleinen"], ["kaffee"]],
                "forbidden": ["groß", "gross"],
            },
            {
                "question": "Zum Mitnehmen oder hier essen?",
                "target_answer": "Zum Mitnehmen, bitte.",
                "required": [["mitnehmen"]],
                "forbidden": ["hier essen"],
            },
            {
                "question": "Möchten Sie noch etwas Süßes?",
                "target_answer": "Ja, ein Stück Kuchen, bitte.",
                "required": [["kuchen"], ["bitte"]],
                "forbidden": ["fahrkarte", "ticket"],
            },
            {
                "question": "Das macht vier Euro zwanzig.",
                "target_answer": "Hier sind fünf Euro.",
                "required": [["euro"], ["fünf", "fuenf", "5"]],
                "forbidden": [],
            },
            {
                "question": "Danke schön. Einen schönen Tag!",
                "target_answer": "Danke, Ihnen auch.",
                "required": [["danke"], ["auch"]],
                "forbidden": [],
            },
        ],
    },
    {
        "id": "supermarket",
        "title": "Shopping at the Supermarket",
        "description": "Practice groceries, finding items, checkout, and payment.",
        "image": "/images/scenes/supermarket-cartoon.png",
        "steps": [
            {
                "question": "Entschuldigung, wo finde ich Milch?",
                "target_answer": "Milch finden Sie im Kühlregal.",
                "required": [["milch"], ["kühlregal", "kuehlregal"]],
                "forbidden": ["bahnhof", "gleis", "fahrkarte"],
            },
            {
                "question": "Brauchen Sie sonst noch etwas?",
                "target_answer": "Ja, ich suche Brot und Eier.",
                "required": [["brot"], ["eier", "ei"]],
                "forbidden": ["ticket", "fahrkarte"],
            },
            {
                "question": "Haben Sie eine Einkaufstasche?",
                "target_answer": "Nein, ich brauche eine Tasche.",
                "required": [["tasche", "einkaufstasche"], ["brauche"]],
                "forbidden": [],
            },
            {
                "question": "Haben Sie eine Kundenkarte?",
                "target_answer": "Nein, ich habe keine Kundenkarte.",
                "required": [["nein"], ["kundenkarte"]],
                "forbidden": ["ja"],
            },
            {
                "question": "Zahlen Sie bar oder mit Karte?",
                "target_answer": "Ich zahle bar.",
                "required": [["bar"]],
                "forbidden": ["karte"],
            },
            {
                "question": "Möchten Sie den Kassenbon?",
                "target_answer": "Ja, bitte.",
                "required": [["ja"], ["bitte"]],
                "forbidden": [],
            },
        ],
    },
    {
        "id": "countryside_trip",
        "title": "A Trip in the Countryside",
        "description": "Practice travel, weather, plans, and simple conversations.",
        "image": "/images/scenes/countryside-cartoon.png",
        "steps": [
            {
                "question": "Wohin fahren wir heute?",
                "target_answer": "Wir fahren heute aufs Land.",
                "required": [["land"], ["fahren"]],
                "forbidden": ["supermarkt", "bahnhof", "bäckerei", "baeckerei"],
            },
            {
                "question": "Wie ist das Wetter heute?",
                "target_answer": "Das Wetter ist schön und sonnig.",
                "required": [["wetter"], ["schön", "schoen", "sonnig"]],
                "forbidden": [],
            },
            {
                "question": "Was möchten wir dort machen?",
                "target_answer": "Wir möchten spazieren gehen und Fotos machen.",
                "required": [["spazieren"], ["fotos", "foto"]],
                "forbidden": ["einkaufen"],
            },
            {
                "question": "Hast du Wasser dabei?",
                "target_answer": "Ja, ich habe Wasser dabei.",
                "required": [["wasser"], ["dabei"]],
                "forbidden": ["nein"],
            },
            {
                "question": "Wann fahren wir zurück?",
                "target_answer": "Wir fahren am Abend zurück.",
                "required": [["abend"], ["zurück", "zurueck"]],
                "forbidden": [],
            },
            {
                "question": "War der Ausflug schön?",
                "target_answer": "Ja, der Ausflug war sehr schön.",
                "required": [["ausflug"], ["schön", "schoen"]],
                "forbidden": [],
            },
        ],
    },
]


def get_topics() -> list[dict[str, str]]:
    return [
        {
            "id": topic["id"],
            "title": topic["title"],
            "description": topic["description"],
            "image": topic["image"],
        }
        for topic in TOPICS
    ]


def get_topic(topic_id: str) -> SceneTopic | None:
    return next((topic for topic in TOPICS if topic["id"] == topic_id), None)


def get_step(topic_id: str, step_index: int) -> SceneStep | None:
    topic = get_topic(topic_id)

    if not topic:
        return None

    steps = topic["steps"]

    if step_index < 0 or step_index >= len(steps):
        return None

    return steps[step_index]


def normalize_text(text: str) -> str:
    text = text.lower().strip()

    replacements = {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "ß": "ss",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def token_set(text: str) -> set[str]:
    normalized = normalize_text(text)
    return {token for token in normalized.split() if len(token) > 1}


def contains_phrase(answer: str, phrase: str) -> bool:
    return normalize_text(phrase) in normalize_text(answer)


def required_groups_match(answer: str, required_groups: list[list[str]]) -> tuple[bool, list[str]]:
    missing: list[str] = []

    for group in required_groups:
        matched = any(contains_phrase(answer, candidate) for candidate in group)

        if not matched:
            missing.append(group[0])

    return len(missing) == 0, missing


def find_forbidden_hit(answer: str, forbidden: list[str]) -> str | None:
    for word in forbidden:
        if contains_phrase(answer, word):
            return word

    return None


def evaluate_answer(step: SceneStep, learner_answer: str) -> dict[str, Any]:
    answer = learner_answer.strip()

    if not answer:
        return {
            "is_correct": False,
            "score": 0,
            "feedback": "Please write an answer first.",
            "corrected_answer": step["target_answer"],
            "should_advance": False,
        }

    forbidden_hit = find_forbidden_hit(answer, step.get("forbidden", []))

    if forbidden_hit:
        return {
            "is_correct": False,
            "score": 35,
            "feedback": (
                "Your sentence is understandable, but it does not match this scene. "
                f"Try to answer with this meaning: {step['target_answer']}"
            ),
            "corrected_answer": step["target_answer"],
            "should_advance": False,
        }

    required_ok, missing = required_groups_match(answer, step.get("required", []))

    expected_tokens = token_set(step["target_answer"])
    answer_tokens = token_set(answer)

    overlap = len(expected_tokens & answer_tokens)
    overlap_ratio = overlap / max(len(expected_tokens), 1)

    if required_ok:
        if overlap_ratio >= 0.35 or len(answer_tokens) <= 5:
            return {
                "is_correct": True,
                "score": max(80, int(overlap_ratio * 100)),
                "feedback": "Good practice. Your meaning fits this scene.",
                "corrected_answer": step["target_answer"],
                "should_advance": True,
            }

        return {
            "is_correct": True,
            "score": 75,
            "feedback": "The meaning is correct. A more natural answer is shown below.",
            "corrected_answer": step["target_answer"],
            "should_advance": True,
        }

    return {
        "is_correct": False,
        "score": max(25, int(overlap_ratio * 100)),
        "feedback": (
            "Almost, but some important meaning is missing. "
            f"Try to include: {', '.join(missing)}."
        ),
        "corrected_answer": step["target_answer"],
        "should_advance": False,
    }


def mask_word(word: str, hint_level: int) -> str:
    clean = word.strip()

    if len(clean) <= 3:
        return clean

    common_words = {
        "ich",
        "wir",
        "sie",
        "der",
        "die",
        "das",
        "ein",
        "eine",
        "einen",
        "und",
        "oder",
        "mit",
        "für",
        "fuer",
        "zum",
        "zur",
        "im",
        "am",
        "ja",
        "nein",
        "bitte",
        "danke",
    }

    normalized = normalize_text(clean)

    if normalized in common_words:
        return clean

    chars = list(clean)

    if hint_level <= 0:
        reveal_count = max(2, len(chars) // 2)
    elif hint_level == 1:
        reveal_count = max(3, int(len(chars) * 0.65))
    else:
        return clean

    result: list[str] = []

    for index, char in enumerate(chars):
        if not char.isalpha():
            result.append(char)
            continue

        if index < reveal_count:
            result.append(char)
        else:
            result.append("_")

    return "".join(result)


def mask_answer(answer: str, hint_level: int = 0) -> str:
    words = answer.split(" ")
    return " ".join(mask_word(word, hint_level) for word in words)


def add_message(session: Session, session_id: int, role: str, content: str) -> ChatMessage:
    message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content,
        created_at=datetime.utcnow(),
    )

    session.add(message)

    return message


def get_messages(session: Session, chat_session_id: int) -> list[dict[str, str]]:
    statement = (
        select(ChatMessage)
        .where(ChatMessage.session_id == chat_session_id)
        .order_by(ChatMessage.id)
    )

    messages = session.exec(statement).all()

    return [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in messages
    ]


def build_state_response(
    session: Session,
    chat_session: ChatSession,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    topic = get_topic(chat_session.topic_id)

    if not topic:
        raise ValueError("Topic not found")

    steps = topic["steps"]
    current_step = min(chat_session.current_step, len(steps) - 1)
    step = steps[current_step]

    base = {
        "session_id": chat_session.id,
        "topic_id": chat_session.topic_id,
        "topic_title": topic["title"],
        "topic_description": topic["description"],
        "topic_image": topic["image"],
        "current_step": chat_session.current_step,
        "total_steps": len(steps),
        "question": step["question"],
        "masked_answer": mask_answer(step["target_answer"], chat_session.hint_level),
        "full_answer": step["target_answer"],
        "hint_level": chat_session.hint_level,
        "finished": chat_session.finished,
        "messages": get_messages(session, chat_session.id),
    }

    if extra:
        base.update(extra)

    return base


def start_session(session: Session, topic_id: str) -> dict[str, Any]:
    topic = get_topic(topic_id)

    if not topic:
        raise ValueError("Topic not found")

    first_step = topic["steps"][0]

    chat_session = ChatSession(
        topic_id=topic_id,
        current_step=0,
        hint_level=0,
        finished=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    session.add(chat_session)
    session.commit()
    session.refresh(chat_session)

    add_message(session, chat_session.id, "ai", first_step["question"])
    session.commit()

    return build_state_response(session, chat_session)


def get_hint(session: Session, session_id: int, hint_level: int | None = None) -> dict[str, Any]:
    chat_session = session.get(ChatSession, session_id)

    if not chat_session:
        raise ValueError("Session not found")

    if chat_session.finished:
        return build_state_response(session, chat_session)

    if hint_level is None:
        chat_session.hint_level = min(chat_session.hint_level + 1, 2)
    else:
        chat_session.hint_level = min(max(hint_level, 0), 2)

    chat_session.updated_at = datetime.utcnow()

    session.add(chat_session)
    session.commit()
    session.refresh(chat_session)

    step = get_step(chat_session.topic_id, chat_session.current_step)

    if not step:
        raise ValueError("Step not found")

    return {
        "session_id": chat_session.id,
        "hint_level": chat_session.hint_level,
        "masked_answer": mask_answer(step["target_answer"], chat_session.hint_level),
        "full_answer": step["target_answer"],
    }


def answer_session(session: Session, session_id: int, learner_answer: str) -> dict[str, Any]:
    chat_session = session.get(ChatSession, session_id)

    if not chat_session:
        raise ValueError("Session not found")

    if chat_session.finished:
        return build_state_response(
            session,
            chat_session,
            {
                "is_correct": True,
                "should_advance": False,
                "score": 100,
                "feedback": "This scene is already finished.",
                "corrected_answer": "",
            },
        )

    topic = get_topic(chat_session.topic_id)

    if not topic:
        raise ValueError("Topic not found")

    steps = topic["steps"]
    step = steps[chat_session.current_step]

    add_message(session, chat_session.id, "user", learner_answer)

    result = evaluate_answer(step, learner_answer)

    feedback_text = result["feedback"]

    if result["is_correct"]:
        feedback_text += f" Natural answer: {result['corrected_answer']}"

    add_message(session, chat_session.id, "system", feedback_text)

    if result["should_advance"]:
        is_last_step = chat_session.current_step >= len(steps) - 1

        if is_last_step:
            chat_session.finished = True
            add_message(
                session,
                chat_session.id,
                "ai",
                "Sehr gut! Diese Szene ist fertig. Du kannst eine andere Szene üben.",
            )
        else:
            chat_session.current_step += 1
            chat_session.hint_level = 0

            next_step = steps[chat_session.current_step]
            add_message(session, chat_session.id, "ai", next_step["question"])
    else:
        chat_session.hint_level = min(chat_session.hint_level + 1, 2)

    chat_session.updated_at = datetime.utcnow()

    session.add(chat_session)
    session.commit()
    session.refresh(chat_session)

    return build_state_response(
        session,
        chat_session,
        {
            "is_correct": result["is_correct"],
            "should_advance": result["should_advance"],
            "score": result["score"],
            "feedback": result["feedback"],
            "corrected_answer": result["corrected_answer"],
        },
    )