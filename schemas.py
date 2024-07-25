from pydantic import BaseModel
from typing import List, Optional


class BookBase(BaseModel):
    title: str
    summary: str
    author_id: int  # Referencing author_id directly

    class Config:
        from_attributes = True  # This allows compatibility with ORM models


class BookList(BookBase):
    id: int

    class Config:
        from_attributes = True  # Ensuring ORM compatibility


class AuthorBase(BaseModel):
    name: str
    bio: str

    class Config:
        from_attributes = True  # Ensuring ORM compatibility


class AuthorList(AuthorBase):
    id: int
    books: List[BookList]  # List of books written by the author

    class Config:
        from_attributes = True  # Ensuring ORM compatibility
