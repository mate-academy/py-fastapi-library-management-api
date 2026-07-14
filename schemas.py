from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class AuthorBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    bio: str = Field(min_length=1)


class AuthorCreate(AuthorBase):
    pass


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    summary: str = Field(min_length=1)
    publication_date: date


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class Author(AuthorBase):
    id: int
    books: list[Book] = []

    model_config = ConfigDict(from_attributes=True)
