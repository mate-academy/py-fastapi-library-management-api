from datetime import date
from typing import Optional, List

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: Optional[str]
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str]


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List[Book] = []

    class Config:
        from_attributes = True
