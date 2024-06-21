from datetime import date
from typing import Optional, List

from pydantic import BaseModel


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
    pass


class Book(BookBase):
    id: int
    author_id: Author

    class Config:
        orm_mode = True
