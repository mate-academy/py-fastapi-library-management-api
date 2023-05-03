from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List["Book"] = []

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class BookUpdate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int
    author: Author

    class Config:
        orm_mode = True
