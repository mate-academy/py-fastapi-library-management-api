from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int
    books: List['BookRead'] = []

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: Optional[datetime] = None
    author_id: int


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    id: int

    class Config:
        from_attributes = True


AuthorRead.update_forward_refs()
