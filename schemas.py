from pydantic import BaseModel
from typing import Optional
from datetime import date

class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorRead(AuthorBase):
    id: int

    class Config:
        from_attributes = True

class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True
