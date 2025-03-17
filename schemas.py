from typing import List
from datetime import date
from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int

    class Config:
        from_attribute = True


class Book(BaseModel):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorRead(AuthorBase):
    id: int
    books: List[str]

    class Config:
        orm_mode = True


class AuthorCreate(AuthorBase):
    pass
