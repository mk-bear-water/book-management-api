from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.api.errors import conflict
from app.core.db import get_db

router = APIRouter(prefix="/authors", tags=["authors"])


@router.post(
    "",
    response_model=schemas.AuthorOut,
    status_code=status.HTTP_201_CREATED,
)
def create_author(
    payload: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    author = models.Author(name=payload.name)

    try:
        db.add(author)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise conflict("Author")

    db.refresh(author)
    return author
