from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: Optional[date] = None
    author_id: int

class BookCreate(BookBase):
    pass

class Book(BookCreate):
    id: int

    class Config:
        orm_mode = True

class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    books: List[Book]

    class Config:
        orm_mode = True
