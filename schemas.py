from datetime import date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class Book(BookCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    ...


class Author(AuthorCreate):
    id: int
    books: List[Book] = []

    model_config = ConfigDict(from_attributes=True)
