from datetime import date

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class BookBase(BaseModel):
    title: str
    summary: str


class BookCreate(BookBase):
    author_id: int
    publication_date: date | None = None


class Book(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

    author_id: int
    publication_date: date
