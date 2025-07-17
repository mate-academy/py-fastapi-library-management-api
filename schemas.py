from pydantic import BaseModel
from typing import List
from datetime import date


class AuthorBase(BaseModel):
    name: str
    bio: str


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class AuthorCreate(AuthorBase):
    pass


class BookCreate(BookBase):
    author_id: int


class AuthorList(AuthorBase):
    id: int
    books: List[BookBase]

    class Config:
        orm_mode = True


class Author(AuthorBase):
    id: int
    books: List[BookBase]


class BookList(BookBase):
    id: int
    author: AuthorBase

    class Config:
        orm_mode = True
