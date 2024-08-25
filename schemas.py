from pydantic import BaseModel
from typing import List
from datetime import date

from db.models import Book


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date

    class Config:
        from_attributes = True


class BookCreate(BookBase):
    author_id: int


class BookList(BookBase):
    id: int

    class Config:
        from_attributes = True


class AutorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AutorBase):
    pass


class Author(AutorBase):
    id: int
    books: List[BookList] = []

    class Config:
        from_attributes = True
