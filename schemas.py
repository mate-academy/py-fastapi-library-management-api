from pydantic import BaseModel

from datetime import date
from typing import List, Optional


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorResponse(AuthorBase):
    id: int
    books: List['BookResponse'] = []

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class BookResponse(BookBase):
    id: int
    author: Optional[AuthorResponse]

    class Config:
        orm_mode = True


AuthorResponse.update_forward_refs()
