from datetime import date

from pydantic import BaseModel, ConfigDict


class Author(BaseModel):
    name: str
    bio: str


class CreateAuthor(Author):
    pass


class AuthorList(Author):
    id: int


class AuthorDetail(Author):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Book(BaseModel):
    title: str
    summary: str
    publication_date: date


class CreateBook(Book):
    author_id: int


class BookList(Book):
    id: int

    model_config = ConfigDict(from_attributes=True)
