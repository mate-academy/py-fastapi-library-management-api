import datetime
from typing import List
from pydantic import BaseModel


class AuthorCreate(BaseModel):
    name: str
    bio: str


class BookRead(BaseModel):
    id: int
    title: str
    summary: str
    publication_date: datetime.date
    author_id: int

    class Config:
        from_attributes = True


class AuthorRead(BaseModel):
    id: int
    name: str
    bio: str
    books: List[BookRead]

    class Config:
        from_attributes = True


class BookCreate(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date
    author_id: int
