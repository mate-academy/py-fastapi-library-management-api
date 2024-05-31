from typing import List, Optional
from datetime import date

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class BookList(BookBase):
    id: int
    author: "AuthorBase"

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    books: Optional[List[BookBase]] = []


class AuthorList(AuthorBase):
    id: int
    books: List[BookBase]

    class Config:
        from_attributes = True
