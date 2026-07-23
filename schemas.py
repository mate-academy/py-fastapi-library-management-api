from datetime import date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

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

    model_config = ConfigDict(from_attributes=True)


# --- Author Schemas ---
class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List[Book] = []

    model_config = ConfigDict(from_attributes=True)
