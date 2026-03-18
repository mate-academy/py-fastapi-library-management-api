from datetime import date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: date


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int
    books: List[BookRead] = []

    model_config = ConfigDict(from_attributes=True)