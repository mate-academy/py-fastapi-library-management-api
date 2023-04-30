from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class PaginatedBooks(BaseModel):
    total: int
    items: List[Book]


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


class PaginatedAuthors(BaseModel):
    total: int
    items: List[Author]


class AuthorListQuery(BaseModel):
    skip: Optional[int] = 0
    limit: Optional[int] = 10
