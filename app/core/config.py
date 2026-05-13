import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "German Vocab Trainer API"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./vocab.db")

    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    USE_LLM: bool = os.getenv("USE_LLM", "true").lower() == "true"

    LLM_MODEL: str = os.getenv(
        "LLM_MODEL",
        "Qwen/Qwen2.5-1.5B-Instruct"
    )

    LLM_LOCAL_DIR: str = os.getenv(
        "LLM_LOCAL_DIR",
        "./models/qwen2.5-1.5b-instruct"
    )

    LLM_PRELOAD_ON_STARTUP: bool = (
        os.getenv("LLM_PRELOAD_ON_STARTUP", "true").lower() == "true"
    )

    LLM_ALLOW_RUNTIME_DOWNLOAD: bool = (
        os.getenv("LLM_ALLOW_RUNTIME_DOWNLOAD", "false").lower() == "true"
    )

    MAX_NEW_TOKENS: int = int(os.getenv("MAX_NEW_TOKENS", "220"))


settings = Settings()