import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

from app.core.config import settings


class LLMNotReadyError(RuntimeError):
    pass


def extract_json(text: str) -> Optional[Any]:
    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{.*\}|\[.*\]", text, re.DOTALL)
    if not match:
        return None

    try:
        return json.loads(match.group(0))
    except Exception:
        return None


def ensure_model_exists_locally():
    local_dir = Path(settings.LLM_LOCAL_DIR)

    required_files = [
        "config.json",
    ]

    if not local_dir.exists():
        raise LLMNotReadyError(
            f"LLM local directory not found: {local_dir}. "
            f"Run: python -m app.scripts.download_model"
        )

    missing_files = [
        file_name for file_name in required_files
        if not (local_dir / file_name).exists()
    ]

    if missing_files:
        raise LLMNotReadyError(
            f"LLM files are incomplete in {local_dir}. "
            f"Missing: {missing_files}. "
            f"Run: python -m app.scripts.download_model"
        )


@lru_cache(maxsize=1)
def get_generator():
    if not settings.USE_LLM:
        return None

    ensure_model_exists_locally()

    try:
        from transformers import pipeline

        model_source = settings.LLM_LOCAL_DIR

        return pipeline(
            "text-generation",
            model=model_source,
            tokenizer=model_source,
            device_map="auto",
            local_files_only=not settings.LLM_ALLOW_RUNTIME_DOWNLOAD,
        )

    except Exception as e:
        raise LLMNotReadyError(
            f"LLM failed to load from local dir: {settings.LLM_LOCAL_DIR}. "
            f"Original error: {e}"
        )


def preload_llm():
    if not settings.USE_LLM:
        print("LLM disabled.")
        return

    print("Preloading LLM...")
    print(f"Model local dir: {settings.LLM_LOCAL_DIR}")

    get_generator()

    print("LLM is ready.")


def generate_text(prompt: str, max_new_tokens: Optional[int] = None) -> str:
    generator = get_generator()

    if generator is None:
        return ""

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful German A1-A2 tutor. "
                "Return concise, valid JSON when requested."
            ),
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    try:
        output = generator(
            messages,
            max_new_tokens=max_new_tokens or settings.MAX_NEW_TOKENS,
            do_sample=True,
            temperature=0.4,
        )

        generated = output[0]["generated_text"]

        if isinstance(generated, list):
            return generated[-1]["content"]

        return str(generated)

    except Exception as e:
        print(f"LLM generation failed: {e}")
        return ""


def generate_examples_with_llm(
    german: str,
    vietnamese: str,
    topic: Optional[str],
    level: str = "A2",
) -> list[str]:
    prompt = f"""
Create 5 simple German example sentences for a beginner learner.

German word: {german}
English meaning / gloss: {vietnamese}
Topic: {topic or "general"}
Level: {level}

Rules:
- Use simple A1-A2 German.
- Use the target word naturally.
- Return only a valid JSON array of strings.
Example:
["Ich fange um acht Uhr an.", "Der Kurs fängt morgen an."]
"""

    raw = generate_text(prompt)
    data = extract_json(raw)

    if isinstance(data, list):
        return [str(x) for x in data][:5]

    return [
        f"Ich benutze das Wort {german} in einem einfachen Satz.",
        f"Kannst du {german} bitte noch einmal sagen?",
        f"Wir lernen heute das Wort {german}.",
        f"Das Wort {german} ist wichtig im Alltag.",
        f"Ich schreibe {german} in mein Heft.",
    ]


def generate_mcq_with_llm(
    german: str,
    vietnamese: str,
    examples: str,
    distractors: list[str],
) -> Optional[dict]:
    prompt = f"""
Create one German vocabulary multiple-choice question.

Target word: {german}
English meaning / gloss: {vietnamese}
Examples:
{examples}

Wrong options:
{", ".join(distractors)}

Return only valid JSON:
{{
  "sentence": "German sentence with _____ instead of the target word",
  "options": ["option1", "option2", "option3", "option4"],
  "answer": "{german}",
  "explanation": "Short explanation in English"
}}

Rules:
- The blank must be _____.
- Options must include the target word.
- Options must contain exactly 4 German words.
- The explanation must be in English.
"""

    raw = generate_text(prompt)
    data = extract_json(raw)

    if isinstance(data, dict):
        if "sentence" in data and "options" in data and "answer" in data:
            return data

    return None


def generate_chat_feedback_with_llm(
    topic_title: str,
    ai_message: str,
    expected_answer: str,
    user_answer: str,
) -> str:
    prompt = f"""
    You are a friendly German A1-A2 tutor.
    
    Topic: {topic_title}
    AI asked: {ai_message}
    Expected answer: {expected_answer}
    User answer: {user_answer}
    
    Give short feedback in English.
    Say whether the answer is acceptable.
    If it is incorrect, provide one corrected simple sentence in English context.
    Maximum 3 sentences.
    """

    raw = generate_text(prompt, max_new_tokens=120)

    if raw.strip():
        return raw.strip()

    return "Your answer is understandable. Try to pay attention to word order and the key vocabulary."
