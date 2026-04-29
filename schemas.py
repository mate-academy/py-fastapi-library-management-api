from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str]


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str
    summary: Optional[str]
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author: Author
    model_config = ConfigDict(from_attributes=True)
