from datetime import date
from typing import List

from pydantic import BaseModel


class AuthorBaseSchema(BaseModel):

    name: str
    bio: str

    model_config = {"from_attributes": True}


class AuthorCreateSchema(AuthorBaseSchema):
    pass


class AuthorCreateResponseSchema(AuthorBaseSchema):
    id: int

class AuthorListSchema(AuthorBaseSchema):
    id: int
    books: List["BookBaseSchema"]


class BookBaseSchema(BaseModel):

    title: str
    summary: str
    publication_date: date


class BookCreateSchema(BookBaseSchema):
    author_id: int

class BookCreateResponseSchema(BookBaseSchema):
    id: int
    author: AuthorBaseSchema
