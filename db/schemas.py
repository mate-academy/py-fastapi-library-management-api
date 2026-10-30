from datetime import date
from typing import List

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass


class AuthorDelete(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List["Book"] = []
    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int


class BookCreate(BookBase):
    author_id: int


class BookUpdate(BookBase):
    pass


class BookDelete(BookBase):
    pass


class Book(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
