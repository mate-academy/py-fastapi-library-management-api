from datetime import date
from typing import Optional

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorUpdate(BaseModel):
    name: Optional[str]
    bio: Optional[str]


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: Optional[date] = None
    author_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class Book(BookBase):
    id: int
    title = str
    summary = str
    author_id = int

    class Config:
        orm_mode = True
