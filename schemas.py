from __future__ import annotations

import datetime

from pydantic import BaseModel

import models


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    pass


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date
    author_id: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int
    
    class Config:
        orm_mode = True


class Author(AuthorBase):
    id: int
    books: list[Book] = []

    class Config:
        orm_mode = True