from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.database import create_db_and_tables
from app.routers import ai, chat, collections, mcq, stats, vocab
from app.services.llm_service import LLMNotReadyError, preload_llm

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

    if settings.USE_LLM and settings.LLM_PRELOAD_ON_STARTUP:
        try:
            preload_llm()
        except LLMNotReadyError as e:
            print("")
            print("LLM is not ready.")
            print(str(e))
            print("")
            raise e


@app.get("/")
def root():
    return {
        "message": "German Vocab Trainer API is running",
        "llm_model": settings.LLM_MODEL,
        "llm_local_dir": settings.LLM_LOCAL_DIR,
        "use_llm": settings.USE_LLM,
        "llm_preload_on_startup": settings.LLM_PRELOAD_ON_STARTUP,
        "llm_allow_runtime_download": settings.LLM_ALLOW_RUNTIME_DOWNLOAD,
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "use_llm": settings.USE_LLM,
    }


app.include_router(collections.router)
app.include_router(vocab.router)
app.include_router(mcq.router)
app.include_router(stats.router)
app.include_router(ai.router)
app.include_router(chat.router)