from pydantic import BaseModel
from typing import Optional
from datetime import date


class AuthorCreate(BaseModel):
    name: str
    bio: Optional[str] = None


class Author(AuthorCreate):
    id: int

    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: Optional[date] = None


class Book(BookCreate):
    id: int
    author_id: int

    class Config:
        orm_mode = True
