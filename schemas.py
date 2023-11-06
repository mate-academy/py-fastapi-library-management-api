from datetime import date
from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    summary: str


class BookCreate(BookBase):
    author_id: int
    publication_date: date


class Book(BookBase):
    id: int
    author: Author

    class Config:
        from_attributes = True
