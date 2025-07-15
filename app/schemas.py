from datetime import date
from typing import List

from pydantic import BaseModel


class AuthorBaseSchema(BaseModel):
    name: str
    bio: str


class AuthorRetrieveSchema(AuthorBaseSchema):
    id: int


class AuthorCreateSchema(AuthorBaseSchema):
    pass


class BookBaseSchema(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreateSchema(BookBaseSchema):
    author_id: int


class BookListSchema(BookBaseSchema):
    id: int

    class Config:
        from_attributes = True


class AuthorListSchema(AuthorBaseSchema):
    id: int
    books: List[BookBaseSchema]

    class Config:
        from_attributes = True
