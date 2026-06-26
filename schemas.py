from datetime import date

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str


class CreateAuthor(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list["Book"]

    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class CreateBook(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)
