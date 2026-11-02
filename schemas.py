from datetime import date

from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    summary: str
    publication_date: date


class Book(BookCreate):
    id: int
    author_id: int

    class Config:
        from_attributes = True


class AuthorCreate(BaseModel):
    name: str
    bio: str


class Author(AuthorCreate):
    id: int
    books: list[Book] = []

    class Config:
        from_attributes = True
