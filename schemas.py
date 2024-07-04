from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: Optional[datetime] = None


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List[Book] = []

    class Config:
        orm_mode = True
