from pydantic import BaseModel
from typing import List
from typing import Optional
from datetime import date

import schemas


class AuthorBase(BaseModel):
    name: str
    bio: str


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class AuthorCreate(AuthorBase):
    pass


class BookCreate(BookBase):
    id: int
    author_id: Optional[int] = None


class AuthorList(AuthorBase):
    id: int
    books: List[BookBase]

    class Config:
        orm_mode = True


class Author(AuthorBase):
    id: int
    books: List[BookBase]


class BookList(BookBase):
    id: int
    author: AuthorBase

    class Config:
        orm_mode = True


class AuthorUpdate(AuthorBase):
    pass


class BookUpdate(BookBase):
    title: Optional[str] = None
    summary: Optional[str] = None
    publication_date: Optional[date] = None
    author_id: Optional[int] = None
