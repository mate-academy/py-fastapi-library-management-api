from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None  # noqa: E501

    publication_date: Optional[date] = None  # noqa: E501


class BookCreate(BookBase):
    pass


class BookOut(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorOut(AuthorBase):
    id: int
    books: List[BookOut] = list  # noqa: E501

    class Config:
        from_attributes = True
