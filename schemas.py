from datetime import date
from pydantic import BaseModel
from typing import List, Optional

# --- Book Schemas ---
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
        from_attributes = True  # вместо orm_mode


# --- Author Schemas ---
class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    books: List[Book] = []

    class Config:
        from_attributes = True  # вместо orm_mode
