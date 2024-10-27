from datetime import date
from typing import Optional

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    name: Optional[str] = None
    bio: Optional[str] = None

    class Config:
        orm_mode = True


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class BookUpdate(BookBase):
    title: Optional[str] = None
    summary: Optional[str] = None
    publication_date: Optional[date] = None
    author_id: Optional[int] = None

    class Config:
        orm_mode = True


class Book(BookBase):
    id: int
    author: Optional[Author] = None

    class Config:
        orm_mode = True
