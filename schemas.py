from datetime import date
from typing import List

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int

    class Config:
        orm_mode = True


class Book(BookBase):
    id: int


class BookCreate(BookBase):
    pass


class AuthorBase(BaseModel):
    name: str
    bio: str

    class Config:
        orm_mode = True


class Author(AuthorBase):
    id: int
    books: List[Book] = []


class AuthorCreate(AuthorBase):
    pass
