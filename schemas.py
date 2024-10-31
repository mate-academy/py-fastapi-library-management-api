from datetime import datetime
from typing import List

from pydantic import BaseModel


class BaseAuthor(BaseModel):
    name: str
    bio: str

class Author(BaseAuthor):
    id: int

    class Config:
        from_attributes = True


class AuthorCreate(BaseAuthor):
    pass


class BaseBook(BaseModel):
    title: str
    summary: str
    publication_date: datetime
    author_id: int

class Book(BaseBook):
    id: int

    class Config:
        from_attributes = True


class BookCreate(BaseBook):
    pass
