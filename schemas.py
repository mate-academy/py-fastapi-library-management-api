from datetime import date

from pydantic import BaseModel
from sqlalchemy import Date


class BookBase(BaseModel):
    title: str
    summary: str | None = None


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    publication_date: date
    author_id: int

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[Book] = []

    class Config:
        from_attributes = True
