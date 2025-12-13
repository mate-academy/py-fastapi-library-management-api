import datetime

from pydantic import BaseModel, ConfigDict


class AuthorBaseSchema(BaseModel):
    name: str
    bio: str


class AuthorCreateSchema(AuthorBaseSchema):
    pass


class AuthorListSchema(AuthorBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int


class BookBaseSchema(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date


class BookCreateSchema(BookBaseSchema):
    author_id: int


class BookListSchema(BookBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author: AuthorListSchema
