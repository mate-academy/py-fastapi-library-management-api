from pydantic import BaseModel
from typing import Optional
from datetime import date


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    publication_date: Optional[date] = None
    author_id: Optional[int] = None


class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None


class AuthorResponse(BaseModel):
    id: int
    name: str
    bio: str
    books: Optional[list[BookResponse]]

    class Config:
        from_attributes = True
