from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: Optional[date] = None

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorRead(AuthorBase):
    id: int
    books: List[BookRead] = []

    class Config:
        from_attributes = True
