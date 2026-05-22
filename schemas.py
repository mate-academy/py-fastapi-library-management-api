from datetime import date
from typing import Optional

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date
    author: Optional[Author] = None


class BookCreate(BookBase):
    author: int


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True
