from pydantic import BaseModel
from datetime import date
from typing import List


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int


class Book(BookCreate):
    id: int
    author_id: int

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List[Book] = []

    class Config:
        orm_mode = True
