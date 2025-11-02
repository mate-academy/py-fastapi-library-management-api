from datetime import date

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorSchema(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str
    summary: str | None = None
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class BookSchema(BookBase):
    id: int
    author: AuthorSchema


class AuthorDetail(AuthorSchema):
    books: list[BookSchema]

    model_config = ConfigDict(from_attributes=True)
