from datetime import date
from typing import Optional
from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: Optional[date] = None
    author_id: int


class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class Book(BookBase):
    id: int

    class Config:
        from_attributes = True