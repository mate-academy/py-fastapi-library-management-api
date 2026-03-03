from datetime import date
from typing import List

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreateSchema(AuthorBase):
    pass


class BookReadSchema(BaseModel):
    id: int
    title: str
    summary: str
    publication_date: date
    author: AuthorBase


class BookCreateSchema(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int
