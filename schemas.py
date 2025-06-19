from datetime import date
from typing import Optional

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorRead(AuthorBase):
    id: int


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookRead(BookBase):
    id: int
    author_id: int


class BookCreate(BookBase):
    author_id: int


class BookUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    publication_date: Optional[date] = None
    author_id: Optional[int] = None
