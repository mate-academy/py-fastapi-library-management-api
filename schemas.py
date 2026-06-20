from pydantic import BaseModel
from datetime import date


class BookBase(BaseModel):
    title: str
    summary: str | None = None
    publication_date: date | None = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    books: list[Book] = []

    class Config:
        from_attributes = True
