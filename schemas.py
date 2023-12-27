from datetime import date
from pydantic import BaseModel
from typing import Optional


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


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
        orm_mode = True
