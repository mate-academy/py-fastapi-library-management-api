from __future__ import annotations

from datetime import date
from typing import List

from pydantic import BaseModel, ConfigDict


class BookShort(BaseModel):
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)


class AuthorShort(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int
    books: List[BookShort] = []

    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str
    summary: str | None = None
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class BookRead(BookBase):
    id: int
    author: AuthorShort

    model_config = ConfigDict(from_attributes=True)
