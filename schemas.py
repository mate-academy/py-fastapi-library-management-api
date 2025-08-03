from datetime import datetime
from typing import List

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime
    author_id: int


class BookList(BookBase):
    id: int

    class Config:
        orm_mode = True


class BookCreate(BookBase):
    pass


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorList(AuthorBase):
    id: int
    books: List[BookList]

    class Config:
        orm_mode = True


class BookDetail(BookBase):
    id: int
    author: AuthorList

    class Config:
        orm_mode = True


class AuthorDetail(AuthorBase):
    id: int
    books: List[BookList]

    class Config:
        orm_mode = True


class AuthorCreate(AuthorBase):
    pass
