from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.database import get_session
from app.models.models import (
    Collection,
    CollectionCreate,
    CollectionRead,
    CollectionUpdate,
    Vocab,
)

router = APIRouter(prefix="/collections", tags=["collections"])


@router.get("", response_model=list[CollectionRead])
def list_collections(session: Session = Depends(get_session)):
    statement = select(Collection).order_by(Collection.created_at.desc())
    return session.exec(statement).all()


@router.post("", response_model=CollectionRead)
def create_collection(
    collection_create: CollectionCreate,
    session: Session = Depends(get_session),
):
    collection = Collection.model_validate(collection_create)

    session.add(collection)
    session.commit()
    session.refresh(collection)

    return collection


@router.put("/{collection_id}", response_model=CollectionRead)
def update_collection(
    collection_id: int,
    collection_update: CollectionUpdate,
    session: Session = Depends(get_session),
):
    collection = session.get(Collection, collection_id)

    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    update_data = collection_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(collection, key, value)

    session.add(collection)
    session.commit()
    session.refresh(collection)

    return collection


@router.delete("/{collection_id}")
def delete_collection(
    collection_id: int,
    session: Session = Depends(get_session),
):
    collection = session.get(Collection, collection_id)

    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    vocabs = session.exec(
        select(Vocab).where(Vocab.collection_id == collection_id)
    ).all()

    for vocab in vocabs:
        vocab.collection_id = None
        session.add(vocab)

    session.delete(collection)
    session.commit()

    return {"deleted": True}