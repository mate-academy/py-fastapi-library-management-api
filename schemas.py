from datetime import datetime

from pydantic import BaseModel

from models import Book


class AuthorBase(BaseModel):
    name: str
    bio: str = None
    books: list[Book] = []


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str = None
    author_id: int


class BookCreate(BookBase):
    pass


class BookList(BookBase):
    id: int
    publication_date: datetime
