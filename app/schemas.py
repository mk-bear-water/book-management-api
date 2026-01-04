from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class AuthorCreate(BaseModel):
    name: str = Field(..., max_length=50)


class AuthorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


class BookCreate(BaseModel):
    title: str = Field(..., max_length=100)
    author_id: UUID


class BookOut(BaseModel):
    id: UUID
    title: str
    author_id: UUID
    author_name: str
