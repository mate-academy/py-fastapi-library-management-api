from datetime import date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None


class AuthorRead(AuthorBase):
    id: int
    books: List["BookRead"]

    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    publication_date: Optional[date] = None


class BookRead(BookBase):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)


AuthorRead.model_rebuild()
