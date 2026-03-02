from datetime import date
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class Author(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
