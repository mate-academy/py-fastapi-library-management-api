from datetime import date
from typing import Optional, List

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: Optional[date] = None


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List[Book] = []

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
