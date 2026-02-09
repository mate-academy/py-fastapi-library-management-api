from datetime import date

from pydantic import BaseModel, ConfigDict


class AuthorBaseSchema(BaseModel):
    name: str
    bio: str


class AuthorCreateUpdateSchema(AuthorBaseSchema):
    pass


class AuthorListSchema(AuthorBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorDetailSchema(AuthorListSchema):
    books: list["BookBaseSchema"]


class BookBaseSchema(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreateUpdateSchema(BookBaseSchema):
    author_id: int


class BookListSchema(BookBaseSchema):
    id: int
    author: AuthorListSchema

    model_config = ConfigDict(from_attributes=True)
