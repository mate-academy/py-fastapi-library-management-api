from pydantic import BaseModel
from typing import Optional
from datetime import date


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
    publication_date: Optional[date] = None


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True
