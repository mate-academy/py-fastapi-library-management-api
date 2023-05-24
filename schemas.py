from datetime import date
from typing import Optional

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: int
    publication_date: Optional[date]


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author = Author

    class Config:
        orm_mode = True
