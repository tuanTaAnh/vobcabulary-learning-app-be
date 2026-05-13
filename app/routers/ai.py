from fastapi import APIRouter

from app.schemas.schemas import GenerateExamplesRequest, GenerateExamplesResponse
from app.services.llm_service import generate_examples_with_llm

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/examples", response_model=GenerateExamplesResponse)
def generate_examples(data: GenerateExamplesRequest):
    examples = generate_examples_with_llm(
        german=data.german,
        vietnamese=data.vietnamese,
        topic=data.topic,
        level=data.level,
    )

    return GenerateExamplesResponse(examples=examples)
