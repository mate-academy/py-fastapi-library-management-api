from typing import List, Optional
from pydantic import BaseModel
from pydantic.schema import date


class BookBase(BaseModel):
    title: str
    summary: Optional[str]
    publication_date: Optional[date]

class BookCreate(BookBase):
    author_id: int

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True

class AuthorBase(BaseModel):
    name: str
    bio: Optional[str]

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    books: List[Book] = []

    class Config:
        orm_mode = True
