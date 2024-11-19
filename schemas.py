from __future__ import annotations

from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class AuthorUpdate(AuthorBase):
    name: Optional[str] = None
    bio: Optional[str] = None

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int = Field(..., gt=0)


class Book(BookBase):
    id: int
    author: Author

    class Config:
        from_attributes = True


class BookUpdate(BookBase):
    title: Optional[str] = None
    summary: Optional[str] = None
    publication_date: Optional[date] = None
    author_id: Optional[int] = None

    class Config:
        from_attributes = True


class DeleteResponse(BaseModel):
    message: str
    deleted_id: int
