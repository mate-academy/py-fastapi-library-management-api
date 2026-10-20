from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    summary: str
    publication_date: date


class BookCreate(BookBase):
    pass


class Book(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int


class AuthorBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    books: list[Book] = Field(default_factory=list)
