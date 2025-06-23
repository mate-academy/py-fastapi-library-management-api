from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


# --- Book schemas ---

class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: Optional[date] = None


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


# --- Author schemas ---

class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List[Book] = Field(default_factory=list)

    class Config:
        orm_mode = True
