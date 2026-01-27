# schemas.py
from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorRead(AuthorBase):
    id: int
    books: List["BookRead"] = []  # Список книг автора

    class Config:
        from_attributes = True



class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: Optional[date] = None

class BookCreate(BookBase):
    author_id: int

class BookRead(BookBase):
    id: int
    author: AuthorRead

    class Config:
        from_attributes = True


AuthorRead.update_forward_refs()
