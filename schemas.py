from typing import List

from pydantic import BaseModel
from datetime import date


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date
    author: str


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List[Book] = []

    class Config:
        orm_mode = True
