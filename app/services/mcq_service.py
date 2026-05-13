import random
from typing import List

from app.models.models import Vocab
from app.schemas.schemas import MCQQuestion
from app.services.llm_service import generate_mcq_with_llm


def simple_blank_sentence(vocab: Vocab) -> str:
    examples = [
        line.strip()
        for line in vocab.examples.split("\n")
        if line.strip()
    ]

    if not examples:
        return f"The word _____ means {vocab.vietnamese}."

    sentence = random.choice(examples)

    if vocab.german in sentence:
        return sentence.replace(vocab.german, "_____")

    return sentence + " _____"


def build_mcq(vocabs: List[Vocab]) -> MCQQuestion:
    if len(vocabs) < 4:
        raise ValueError("Need at least 4 words to generate an MCQ.")

    valid_vocabs = [v for v in vocabs if v.examples.strip()]

    target = random.choice(valid_vocabs or vocabs)

    wrong_options = [v.german for v in vocabs if v.id != target.id]
    distractors = random.sample(wrong_options, 3)

    llm_mcq = generate_mcq_with_llm(
        german=target.german,
        vietnamese=target.vietnamese,
        examples=target.examples,
        distractors=distractors,
    )

    if llm_mcq:
        options = llm_mcq["options"]

        if target.german not in options:
            options = options[:3] + [target.german]

        random.shuffle(options)

        return MCQQuestion(
            vocab_id=target.id,
            sentence=llm_mcq["sentence"],
            options=options[:4],
            answer=target.german,
            explanation=llm_mcq.get("explanation"),
        )

    options = distractors + [target.german]
    random.shuffle(options)

    return MCQQuestion(
        vocab_id=target.id,
        sentence=simple_blank_sentence(target),
        options=options,
        answer=target.german,
        explanation=f"The correct answer is '{target.german}', which means '{target.vietnamese}'.",
    )
