from typing import Optional, List
from datetime import date
from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: date


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: Optional[List[Book]] = None

    class Config:
        from_attributes = True
