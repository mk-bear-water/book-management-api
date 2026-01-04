import uuid

from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[str] = mapped_column(
        CHAR(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )

    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = "books"
    __table_args__ = (
        UniqueConstraint("author_id", "title", name="uq_books_author_id_title"),
    )

    id: Mapped[str] = mapped_column(
        CHAR(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    author_id: Mapped[str] = mapped_column(
        CHAR(36),
        ForeignKey("authors.id"),
        nullable=False,
    )

    author: Mapped[Author] = relationship(back_populates="books")


Index("ix_books_author_id", Book.author_id)
