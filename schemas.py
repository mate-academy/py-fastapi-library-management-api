from datetime import date
from typing import Optional
from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: Optional[str]
    publication_date: Optional[date]
    author_id: int


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None
    books: list = []


class Author(AuthorBase):
    id: int
    books: list[Book] = []

    class Config:
        orm_mode = True
