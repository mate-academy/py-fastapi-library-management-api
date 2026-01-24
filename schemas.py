from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime
    author_id: int


class Book(BookBase):
    id: int
    author: "AuthorBase"
    model_config = ConfigDict(from_attributes=True)


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    title: Optional[str] = None
    summary: Optional[str] = None
    publication_date: Optional[str] = None
    author_id: Optional[int] = None


class AuthorBase(BaseModel):
    name: str
    bio: str


class Author(AuthorBase):
    id: int
    books: List[BookBase] = []
    model_config = ConfigDict(from_attributes=True)


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    id: Optional[int] = None
    name: Optional[str] = None
    bio: Optional[str] = None
    books: Optional[List[BookBase]] = None
