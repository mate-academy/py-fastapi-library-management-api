from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str]


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: Optional[date]


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List[Book] = []

    class Config:
        orm_mode = True
