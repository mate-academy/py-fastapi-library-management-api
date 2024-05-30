from pydantic import BaseModel
from typing import Optional
import datetime


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date
    author_id: int


class BookCreate(BookBase):
    pass


class Author(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class Book(BookBase):
    id: int
    author: Optional[Author]

    class Config:
        from_attributes = True
