from datetime import date
from typing import List

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class BookBase(BaseModel):
    title: str
    summary: str | None = None
    publication_date: date


class AuthorCreate(AuthorBase):
    pass


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class Author(AuthorBase):
    id: int
    books: List[Book] = []

    class Config:
        orm_mode = True
