from typing import Optional
from pydantic import BaseModel
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


class AuthorList(BaseModel):
    items: list[Author]
    total: int


class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: date
    author_id: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class BookList(BaseModel):
    items: list[Book]
    total: int
