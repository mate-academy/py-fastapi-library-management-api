from datetime import date

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class CreateAuthor(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class BooksBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class CreateBook(BooksBase):
    author_id: int


class Book(BooksBase):
    id: int
    author: Author

    class Config:
        from_attributes = True
