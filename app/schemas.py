from __future__ import annotations
from datetime import date

from pydantic import BaseModel


class BookSchema(BaseModel):
    title: str
    summary: str
    publication_data: date
    author_id: int


class BookGetSchema(BookSchema):
    id: int


class CreateBookSchema(BookSchema):
    pass


class AuthorSchema(BaseModel):
    name: str
    bio: str


class AuthorGetSchema(AuthorSchema):
    id: int


class CreateAuthorSchema(AuthorSchema):
    pass
