from datetime import date
from typing import List
from pydantic import BaseModel, ConfigDict


# ---------- BOOK SCHEMAS
class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    pass


class BookRead(BaseModel):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)


# ---------- AUTHOR SCHEMAS
class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int
    books: List[BookRead] = []

    model_config = ConfigDict(from_attributes=True)
