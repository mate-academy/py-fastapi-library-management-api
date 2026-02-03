from __future__ import annotations

from datetime import date
from typing import List

from pydantic import BaseModel, ConfigDict, Field


# --------- Books ---------
class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    summary: str = Field(min_length=1, max_length=2000)
    publication_date: date


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int


# --------- Authors ---------
class AuthorBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    bio: str = Field(min_length=1, max_length=2000)


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    books: List[BookRead] = []
