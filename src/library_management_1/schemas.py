from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    summary: str = Field(default="", max_length=2000)
    publication_date: date


class BookCreate(BookBase):
    pass

class Book(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int


class AuthorBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    bio: str = Field(default="", max_length=2000)


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    books: list[Book] = []
