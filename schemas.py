from datetime import date
from typing import List

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str | None = None
    publication_date: date


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorResponse(AuthorBase):
    id: int
    books: List[BookResponse]

    class Config:
        from_attributes = True
