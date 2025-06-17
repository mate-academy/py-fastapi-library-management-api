from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional


class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    summary: Optional[str] = None
    publication_date: date

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True

class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1)
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    books: List[Book] = Field(default_factory=list)

    class Config:
        from_attributes = True
