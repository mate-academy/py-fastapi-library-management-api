import datetime
from typing import List

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author: "AuthorWithId"

    class Config:
        orm_mode = True


class BookWithId(BookBase):
    id: int


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List["BookWithId"] = []

    class Config:
        orm_mode = True


class AuthorWithId(AuthorBase):
    id: int
