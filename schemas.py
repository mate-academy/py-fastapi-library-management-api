from datetime import date
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    book_ids: List[int] = Field(default_factory=list)


class Author(AuthorBase):
    id: int
    books: List["BookShort"] = []


    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookShort(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author: AuthorBase

    model_config = ConfigDict(from_attributes=True)

Author.model_rebuild()
