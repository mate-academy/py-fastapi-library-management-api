from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class AuthorBase(BaseModel):
    name: str = Field(example="Emily Johnson")
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    model_config = ConfigDict()

    id: int


class ValidationErrorResponse(BaseModel):
    message: str = Field(example="Detail of validation error")


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    model_config = ConfigDict()

    id: int
    author: Author
