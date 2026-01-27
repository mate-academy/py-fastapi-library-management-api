from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import List, Optional


class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: date
    author_id: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
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
    books: List[Book] = []

model_config = ConfigDict(from_attributes=True)
