from datetime import date
from typing import List

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    author_id: int


class BookDetail(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class BookList(BaseModel):
    id: int


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List[int] = []

    class Config:
        orm_mode = True
