from typing import List

from pydantic import BaseModel, ConfigDict


class AuthorBaseSchema(BaseModel):
    name: str
    bio: str


class AuthorReadSchema(AuthorBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int


class BookBaseSchema(BaseModel):
    title: str
    summary: str
    author_id: int
    publication_date: str


class BookReadSchema(BookBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int


class AuthorDetailReadSchema(AuthorReadSchema):
    model_config = ConfigDict(from_attributes=True)

    books: List[BookReadSchema] = []
