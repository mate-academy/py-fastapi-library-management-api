from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class AuthorBook(BaseModel):
    id: int
    name: str


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author: AuthorBook
    model_config = ConfigDict(from_attributes=True)
