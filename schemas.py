from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(max_length=255)
    summary: str
    publication_date: date


class BookCreate(BookBase):
    pass


class BookSchema(BookBase):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorBase(BaseModel):
    name: str = Field(max_length=255)
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorSchema(AuthorBase):
    id: int
    books: list[BookSchema] = []

    model_config = ConfigDict(from_attributes=True)
