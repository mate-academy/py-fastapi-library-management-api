from datetime import date
from typing import Optional

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorList(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int
    pass


class AuthorRetrive(AuthorBase):
    id: int
    books: Optional[list[BookBase]] = None

    class Config:
        from_attributes = True


class BookList(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True


class BookRetrive(BookBase):
    id: int
    author: AuthorBase

    class Config:
        from_attributes = True
