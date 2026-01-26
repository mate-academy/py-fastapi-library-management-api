from datetime import date

from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Book(BookBase):
    id: int
    author: AuthorBase

    model_config = ConfigDict(from_attributes=True)


class Author(AuthorBase):
    id: int
    books: list[Book]

    model_config = ConfigDict(from_attributes=True)
