from datetime import date
from typing import List

from pydantic import BaseModel, Field


class AuthorBase(BaseModel):
    name: str = Field(example="Emily Johnson")
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class ValidationErrorResponse(BaseModel):
    field: str = Field(example="Field_name")
    message: str = Field(example="Detail of validation error")


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author: Author

    class Config:
        orm_model = True
