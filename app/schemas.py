from typing import List, Optional
from datetime import date

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: Optional[date] = None
    author_id: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id_: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id_: int
    books: List[Book] = []

    class Config:
        orm_mode = True
