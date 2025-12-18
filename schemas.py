import datetime
from typing import List
from pydantic import BaseModel, ConfigDict


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
    author_id: int


class Book(BookBase):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class Author(AuthorBase):
    id: int
    books: List[Book]

    model_config = ConfigDict(from_attributes=True)
