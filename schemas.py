from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import List, Optional


class BookBase(BaseModel):
    title: str
    summary: str = None
    publication_date: date
    author_id: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorBase(BaseModel):
    name: str
    bio: str = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List[Book] = []

    model_config = ConfigDict(from_attributes=True)
