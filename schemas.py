import datetime
from pydantic import BaseModel
from typing import List


class AuthorBase(BaseModel):
    name: str
    bio: str


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date


class AuthorCreate(AuthorBase):
    pass


class BookCreate(BookBase):
    authors: List[int]


class Author(AuthorBase):
    id: int
    books: List[BookBase]

    class Config:
        orm_mode = True


class Book(BookBase):
    id: int
    authors: List[Author]

    class Config:
        orm_mode = True
