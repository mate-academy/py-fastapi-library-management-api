from datetime import date

from pydantic import BaseModel, ConfigDict


class Author(BaseModel):
    name: str
    bio: str


class AuthorCreate(Author):
    pass


class AuthorRead(Author):
    id: int
    model_config = ConfigDict(from_attributes=True)


class Book(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(Book):
    pass


class BookRead(Book):
    id: int
    author_id: int
    model_config = ConfigDict(from_attributes=True)
