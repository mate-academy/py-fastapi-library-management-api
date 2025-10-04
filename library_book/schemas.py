from pydantic import BaseModel
from datetime import date
from typing import List
from library_book.models import PackagingType


class AuthorCreate(BaseModel):
    name: str
    bio: str

class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date
    packaging_type: str

    class Config:
        orm_mode = True

class Book(BookBase):
    id: int
    author_id: int

class Author(BaseModel):
    id: int
    name: str
    bio: str
    books: List[Book] = []

    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    title: str
    summary: str
    publication_date: date
    packaging_type: PackagingType
