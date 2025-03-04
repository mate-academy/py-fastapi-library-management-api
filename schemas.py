from pydantic import BaseModel, ConfigDict
from datetime import datetime

import models


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime

    _model_class = models.Book


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorBase(BaseModel):
    name: str
    bio: str

    _model_class = models.Author


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[Book] = []

    model_config = ConfigDict(from_attributes=True)
