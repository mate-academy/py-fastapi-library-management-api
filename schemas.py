import datetime
from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)

    id: int
    books: List[BookBase]


class Book(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    authors: List[Author]
