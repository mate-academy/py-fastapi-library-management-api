from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List["Book"] = []

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: Optional[date] = None


class BookCreate(BookBase):
    author: str


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


Author.update_forward_refs()
