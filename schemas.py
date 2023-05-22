from typing import List

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: str
    author_id: int

    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    pass


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class BookPaginated(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[Book]

    class Config:
        orm_mode = True


class BookFilter(BaseModel):
    author_id: int


class AuthorBase(BaseModel):
    name: str
    bio: str
    books: List[Book]

    class Config:
        orm_mode = True


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class Pagination(BaseModel):
    total: int
    skip: int
    limit: int


class AuthorPaginated(BaseModel):
    pagination: Pagination
    items: List[Author]

    class Config:
        orm_mode = True
