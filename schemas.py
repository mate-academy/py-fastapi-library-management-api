from datetime import date
from typing import Optional

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author: Author

    class Config:
        from_attributes = True
