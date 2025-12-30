from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional


# Author schemas
class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


# Book schemas
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    summary: Optional[str] = Field(None, max_length=1000)
    publication_date: date
    author_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    summary: Optional[str] = Field(None, max_length=1000)
    publication_date: Optional[date] = None
    author_id: Optional[int] = None


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


# Simple author schema for book listings (без bio)
class AuthorSimple(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# Response schemas with relationships
class AuthorWithBooks(Author):
    books: List[Book] = []


class BookWithAuthor(Book):
    author: Author


# NEW: Book with simple author info (для списку книг)
class BookWithSimpleAuthor(Book):
    author: AuthorSimple
