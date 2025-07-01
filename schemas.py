from datetime import date
from typing import List
from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class AuthorBase(BaseModel):
    name: str
    bio: str
    books: List[Book] = Field(default_factory=list)


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    model_config = {
        "from_attributes": True
    }
