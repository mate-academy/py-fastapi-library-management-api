from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import List

class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    author_id: int
    model_config = ConfigDict(from_attributes=True)

class AuthorBase(BaseModel):
    name: str
    bio: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    books: List[Book] = []
    model_config = ConfigDict(from_attributes=True)
