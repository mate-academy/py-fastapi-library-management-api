from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from typing import Optional, List


# Book Schemas
class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: date


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)


# Author Schemas
class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorResponse(AuthorBase):
    id: int
    books: List[BookResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


# Simplified author response without books (for book responses)
class AuthorSimple(BaseModel):
    id: int
    name: str
    bio: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# Extended book response with author details
class BookWithAuthor(BookResponse):
    author: AuthorSimple

    model_config = ConfigDict(from_attributes=True)
