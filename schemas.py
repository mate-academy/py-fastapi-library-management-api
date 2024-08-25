from datetime import date

from pydantic import BaseModel

from models import Book


class Author(BaseModel):
    name: str
    bio: str


class AuthorCreate(Author):
    pass


class Author(Author):
    id: int
    books: Book

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True
