from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.api.errors import conflict, not_found
from app.core.db import get_db

router = APIRouter(prefix="/books", tags=["books"])


def _to_book_out(book: models.Book, author: models.Author) -> schemas.BookOut:
    return schemas.BookOut(
        id=UUID(book.id),
        title=book.title,
        author_id=UUID(book.author_id),
        author_name=author.name,
    )


@router.post(
    "",
    response_model=schemas.BookOut,
    status_code=status.HTTP_201_CREATED,
)
def create_book(
    payload: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    author_stmt = (
        select(models.Author)
        .where(models.Author.id == str(payload.author_id))
    )
    author = db.scalars(author_stmt).first()
    if not author:
        raise not_found("Author")

    book = models.Book(
        title=payload.title,
        author_id=str(payload.author_id),
    )
    try:
        db.add(book)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise conflict("Book")
    db.refresh(book)

    return _to_book_out(book, author)


@router.get("", response_model=list[schemas.BookOut])
def list_books(db: Session = Depends(get_db)):
    stmt = (
        select(models.Book, models.Author)
        .join(models.Author, models.Book.author_id == models.Author.id)
        .order_by(
            models.Author.name.asc(),
            models.Book.title.asc(),
        )
    )
    rows = db.execute(stmt).all()

    return [
        _to_book_out(book, author)
        for book, author in rows
    ]


@router.get("/{book_id}", response_model=schemas.BookOut)
def get_book(book_id: UUID, db: Session = Depends(get_db)):
    stmt = (
        select(models.Book, models.Author)
        .join(models.Author, models.Book.author_id == models.Author.id)
        .where(models.Book.id == str(book_id))
    )
    row = db.execute(stmt).first()
    if not row:
        raise not_found("Book")

    book, author = row
    return _to_book_out(book, author)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: UUID, db: Session = Depends(get_db)):
    stmt = (
        select(models.Book)
        .where(models.Book.id == str(book_id))
    )
    book = db.scalars(stmt).first()
    if not book:
        raise not_found("Book")

    db.delete(book)
    db.commit()
