from datetime import date

from pydantic import BaseModel, ConfigDict


class AuthorCreate(BaseModel):
    name: str
    bio: str


class AuthorRead(AuthorCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class BookCreate(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookRead(BookCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    author_id: int
