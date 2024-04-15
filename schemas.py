from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int


class BookAuthorCreate(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class AuthorReadDetail(AuthorRead):
    books: List[BookRead]
