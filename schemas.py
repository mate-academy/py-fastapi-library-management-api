from datetime import date
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    summary: str = Field(min_length=1, max_length=300)
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    bio: str = Field(min_length=1, max_length=100)


class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
