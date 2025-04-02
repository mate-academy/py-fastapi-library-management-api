from datetime import date
from typing import Optional

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorRetrieve(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class AuthorList(BaseModel):
    authors: list[AuthorRetrieve]
    total_items: int
    total_pages: int
    prev_page: Optional[str]
    next_page: Optional[str]

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class BookRetrieve(BookBase):
    id: int
    author: AuthorRetrieve

    class Config:
        from_attributes = True


class BookList(BaseModel):
    books: list[BookRetrieve]
    total_items: int
    total_pages: int
    prev_page: Optional[str]
    next_page: Optional[str]

    class Config:
        from_attributes = True