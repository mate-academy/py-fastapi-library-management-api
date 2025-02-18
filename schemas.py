from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Author(BaseModel):
    name: str
    bio: str
    books: list[str] = []

    class Config:
        orm_mode = True

class Book(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int

    class Config:
        orm_mode = True

class AuthorCreate(Author):
    pass

class BookCreate(Book):
    pass