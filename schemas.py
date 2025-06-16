from datetime import date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: Optional[date]
    author_id: int


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorDetails(AuthorRead):
    books: List[BookRead] = []


class BookDetails(BookRead):
    author: Optional[AuthorRead] = None
