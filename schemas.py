from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional


class BookBase(BaseModel):
    title: str
    summary: Optional[str] = Field(default=None)
    publication_date: date


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int

    model_config = {
        "from_attributes": True
    }


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = Field(default=None)


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List[Book] = Field(default_factory=list)

    model_config = {
        "from_attributes": True
    }
