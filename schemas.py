from pydantic import BaseModel
from datetime import date


class BookBase(BaseModel):
    title: str
    summary: str | None = None
    publication_date: date

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None

    class Config:
        orm_mode = True


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author: AuthorBase


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[BookBase] = []
