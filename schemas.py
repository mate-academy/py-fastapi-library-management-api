from datetime import date

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BaseBook(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BaseBook):
    author_id: int


class Book(BookCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
