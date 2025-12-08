from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class BookSchema(BaseModel):
    title: str
    summary: str
    publication_date: date

    model_config = {
        "from_attributes": True
    }


class BookCreateSchema(BookSchema):
    author: str


class AuthorSchema(BaseModel):
    name: str

    model_config = {
        "from_attributes": True
    }


class AuthorCreateSchema(AuthorSchema):
    bio: str


class AuthorListItemSchema(BaseModel):
    id: int
    name: str
    bio: str
    books: List[BookSchema]

    model_config = {
        "from_attributes": True,
    }


class AuthorListResponseSchema(BaseModel):
    authors: List[AuthorListItemSchema]
    total_items: int

    model_config = {
        "from_attributes": True,
    }


class AuthorDetailSchema(AuthorSchema):
    id: int
    name: str
    bio: str
    books: List[BookSchema]

    model_config = {
        "from_attributes": True,
    }


class BookListItemSchema(BaseModel):
    id: int
    title: str
    summary: str
    publication_date: date

    model_config = {
        "from_attributes": True,
    }


class BookListResponseSchema(BaseModel):
    books: List[BookListItemSchema]
    total_items: int

    model_config = {
        "from_attributes": True,
    }


class BookDetailSchema(BookSchema):
    id: int
    title: str
    summary: str
    publication_date: date
    author: AuthorSchema

    model_config = {
        "from_attributes": True,
    }


class BookQueryParamsSchema(BaseModel):
    author_id: int | None = Field(None)
