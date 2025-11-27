from datetime import date

from pydantic import BaseModel


class Author(BaseModel):
    name: str
    bio: str


class AuthorCreate(Author):
    pass


class AuthorList(Author):
    id: int


class Book(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int


class BookCreate(Book):
    pass


class BookList(Book):
    id: int
