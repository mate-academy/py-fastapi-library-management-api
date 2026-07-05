from typing import List

from pydantic import BaseModel
from datetime import date


class Book(BaseModel):
    id: int
    title: str
    summary: str
    publication_date: date
    author_id: int

    class Config:
        orm_mode = True


class Author(BaseModel):
    id: int
    name: str
    bio: str
    books: List[Book]

    class Config:
        orm_mode = True


class AuthorCreate(BaseModel):
    name: str
    bio: str


class BookCreate(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int