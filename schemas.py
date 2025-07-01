from datetime import date

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list["BookBase"]

    class Config:
        from_attributes = True


class AuthorList(BaseModel):
    page: int
    per_page: int
    total_pages: int
    authors: list[Author]


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author: AuthorBase

    class Config:
        from_attributes = True


class BookList(BaseModel):
    page: int
    per_page: int
    total_pages: int
    books: list[Book]


Book.model_rebuild()
Author.model_rebuild()
