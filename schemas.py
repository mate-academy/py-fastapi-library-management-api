from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import List, Optional


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: date

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)
