import datetime

from pydantic import BaseModel
from typing_extensions import List


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorForBook(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class BookBase(BaseModel):
    title: str
    summary: str | None = None
    publication_date: datetime.date


class Author(AuthorBase):
    id: int
    books: List[BookBase] = []

    class Config:
        from_attributes = True


class BookCreate(BookBase):
    author_id: int


class BookDetail(BookBase):
    id: int
    author: AuthorBase


class Book(BookBase):
    id: int
    author: AuthorForBook

    class Config:
        from_attributes = True
