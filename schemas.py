from __future__ import annotations
from datetime import date

from pydantic import BaseModel, ConfigDict


class AuthorBaseModel(BaseModel):
    name: str
    bio: str


class AuthorCreateModel(AuthorBaseModel):
    ...


class AuthorListRetrieveModel(AuthorBaseModel):
    id: int
    books: list[BookListRetrieveModel]

    model_config = ConfigDict(from_attributes=True)


class BookBaseModel(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int


class BookCreateModel(BookBaseModel):
    ...


class BookListRetrieveModel(BookBaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)
