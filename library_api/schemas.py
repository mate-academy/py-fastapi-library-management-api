from pydantic import BaseModel
from datetime import date
from typing import List, Optional


# --- Book Schemas ---
class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: date


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True


# --- Author Schemas ---
class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorResponse(AuthorBase):
    id: int
    books: List[BookResponse] = []

    class Config:
        from_attributes = True
