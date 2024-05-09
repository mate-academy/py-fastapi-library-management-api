from datetime import date

from pydantic import BaseModel
from typing import List, Optional


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int
    books: List["BookRead"] = []

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class BookRead(BookBase):
    id: int
    author: AuthorRead

    class Config:
        orm_mode = True


AuthorRead.update_forward_refs()
