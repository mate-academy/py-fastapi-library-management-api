from datetime import datetime

from pydantic import BaseModel

from db.models import CoverType


class AuthorShort(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class BookBase(BaseModel):
    title: str
    author: AuthorShort
    summary: str
    publication_date: datetime
    cover_type: CoverType


class BookCreate(BaseModel):
    title: str
    summary: str
    publication_date: datetime
    cover_type: CoverType
    author_id: int

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True

class BookForAuthor(BookBase):
    id: int

class AuthorBase(BaseModel):
    name: str
    bio: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    books: list[BookForAuthor] = []

    class Config:
        from_attributes = True

