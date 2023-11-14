from datetime import date

from pydantic import BaseModel


class AuthorCreate(BaseModel):
    name: str
    bio: str


class Author(AuthorCreate):
    id: int

    class Config:
        from_attributes = True


class BookCreate(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int


class Book(BookCreate):
    id: int

    class Config:
        from_attributes = True

