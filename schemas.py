from datetime import date

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int


class BookList(BaseModel):
    title: str
    author_id: int
    publication_date: date


class BookRetrieve(BaseModel):
    title: str
    summary: str
    publication_date: date
    author: AuthorBase


class AuthorList(AuthorBase):
    bio: str


class AuthorRetrieve(AuthorList):
    book: list[BookBase]


class AuthorCreate(AuthorList):
    pass
