from pydantic import BaseModel
from datetime import date
from typing import List


# Author schemas
class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class AuthorWithBooks(Author):
    books: List["Book"] = []


# Book schemas
class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True


class BookWithAuthor(Book):
    author: Author


# Update forward references
AuthorWithBooks.model_rebuild()
