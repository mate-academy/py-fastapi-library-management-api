from pydantic import BaseModel
from typing import Optional
from datetime import date


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int  # noqa:VNE003

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int  # noqa:VNE003

    class Config:
        from_attributes = True
