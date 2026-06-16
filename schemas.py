from __future__ import annotations

from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author: Author


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class AuthorWithBooks(Author):
    model_config = ConfigDict(from_attributes=True)

    books: list[Book] = Field(default_factory=list)
