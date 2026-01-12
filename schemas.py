from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# --- Book Schemas ---
class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True  # Allows Pydantic to read data from ORM objects

# --- Author Schemas ---
class AuthorBase(BaseModel):
    name: str
    bio: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    books: List[Book] = []  # Nested list of books

    class Config:
        from_attributes = True
