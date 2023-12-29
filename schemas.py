from typing import List, Optional
from pydantic import BaseModel
from datetime import date


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class AuthorUpdate(AuthorBase):
    name: Optional[str] = None
    bio: Optional[str] = None


class AuthorOut(AuthorBase):
    id: int
    name: str
    bio: str


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author: Author

    class Config:
        orm_mode = True


class PaginatedResponse(BaseModel):
    total: int
    items: List[Author or Book]


class BookUpdate(BookBase):
    title: Optional[str] = None
    summary: Optional[str] = None
    publication_date: Optional[date] = None


class BookOut(BookBase):
    id: int
    title: str
    summary: str
    publication_date: date
