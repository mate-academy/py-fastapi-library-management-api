from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: Optional[date]
    author_id: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str
    bio: str

    class Config:
        from_attributes = True


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[Book]

    class Config:
        from_attributes = True
