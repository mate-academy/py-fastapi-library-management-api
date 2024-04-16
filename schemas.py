from typing import List
from pydantic import BaseModel
from datetime import datetime


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime

    class Config:
        orm_mode = True


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int


class AuthorBase(BaseModel):
    name: str
    bio: str

    class Config:
        orm_mode = True


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List[Book] = []


class AuthorWithBooks(Author):
    books: List[Book] = []
