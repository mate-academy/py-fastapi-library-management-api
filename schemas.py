from datetime import date

from pydantic import BaseModel, ConfigDict


class AuthorTypeBase(BaseModel):
    name: str
    bio: str


class AuthorTypeCreate(AuthorTypeBase):
    pass


class Author(AuthorTypeBase):
    id: int
    books: list["Book"] = []

    model_config = ConfigDict(from_attributes=True)


class BookTypeBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookTypeCreate(BookTypeBase):
    author_id: int


class Book(BookTypeBase):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)
