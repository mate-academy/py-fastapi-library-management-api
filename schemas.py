import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    books: List["Book"] = []


class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: Optional[datetime.date] = None


class BookCreate(BookBase):
    pass


class Book(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int
    author: Optional[Author] = None
