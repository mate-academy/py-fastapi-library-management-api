from datetime import datetime
from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    summary: str
    publication_date: datetime
    author_id: int


class Book(BookCreate):
    id: int

    class Config:
        from_attributes = True


class AuthorCreate(BaseModel):
    name: str
    bio: str


class Author(AuthorCreate):
    id: int

    class Config:
        from_attributes = True


class AuthorDetail(Author):
    books: list[Book] | None = None

    class Config:
        from_attributes = True


class BookDetail(BaseModel):
    id: int
    title: str
    summary: str
    publication_date: datetime
    author: Author
