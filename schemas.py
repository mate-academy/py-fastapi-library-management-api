from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class AuthorBase(BaseModel):
    name: str = Field(..., example="J.K. Rowling")
    bio: Optional[str] = Field(None, example="Author of the Harry Potter series")


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str = Field(..., example="Harry Potter and the Philosopher's Stone")
    summary: Optional[str] = Field(
        None, example="The first book in the Harry Potter series"
    )
    publication_date: Optional[date] = Field(None, example="1997-06-26")


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author: Author

    class Config:
        orm_mode = True
