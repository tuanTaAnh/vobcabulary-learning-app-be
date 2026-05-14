import os
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, Header, HTTPException, UploadFile
from sqlmodel import Session

from app.db.database import get_session
from app.services.excel_import_service import import_excel_to_collection


router = APIRouter(prefix="/import", tags=["import"])


def verify_import_token(
    x_import_token: Optional[str] = Header(default=None),
) -> None:
    expected_token = os.getenv("IMPORT_API_TOKEN")

    if not expected_token:
        return

    if x_import_token != expected_token:
        raise HTTPException(status_code=401, detail="Invalid import token.")


@router.post("/excel")
async def import_excel(
    file: UploadFile = File(...),
    collection_name: str = Form(default="German Vocab"),
    collection_description: str = Form(default="Imported from Excel"),
    collection_icon: str = Form(default="🇩🇪"),
    default_topic: Optional[str] = Form(default=None),
    mode: str = Form(default="update"),
    sheet_name: Optional[str] = Form(default=None),
    session: Session = Depends(get_session),
    _: None = Depends(verify_import_token),
):
    filename = file.filename or ""

    if not filename.lower().endswith((".xlsx", ".xlsm")):
        raise HTTPException(
            status_code=400,
            detail="Please upload an .xlsx or .xlsm Excel file.",
        )

    try:
        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        result = import_excel_to_collection(
            session=session,
            file_bytes=file_bytes,
            collection_name=collection_name,
            collection_description=collection_description,
            collection_icon=collection_icon,
            default_topic=default_topic,
            mode=mode,
            sheet_name=sheet_name,
        )

        return result

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Excel import failed: {exc}",
        ) from exc