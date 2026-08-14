from pydantic import BaseModel
from datetime import date
from typing import List


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List[Book] = []  # ✅ тепер без лапок, чисто й зрозуміло

    class Config:
        orm_mode = True
