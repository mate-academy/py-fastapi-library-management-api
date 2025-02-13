import datetime
from typing import List, Optional
from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: Optional[datetime.date] = None

class BookCreate(BookBase):
    author_id: int

class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True

class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None
    books: Optional[List[Book]] = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True
