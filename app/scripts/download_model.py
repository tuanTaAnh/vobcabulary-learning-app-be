from pathlib import Path

from huggingface_hub import snapshot_download

from app.core.config import settings


def main():
    local_dir = Path(settings.LLM_LOCAL_DIR)
    local_dir.mkdir(parents=True, exist_ok=True)

    print("Downloading model...")
    print(f"Model ID: {settings.LLM_MODEL}")
    print(f"Local dir: {local_dir.resolve()}")

    snapshot_download(
        repo_id=settings.LLM_MODEL,
        local_dir=str(local_dir),
        local_dir_use_symlinks=False,
    )

    print("Model download complete.")


if __name__ == "__main__":
    main()