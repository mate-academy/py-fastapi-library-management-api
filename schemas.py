import datetime

from pydantic import BaseModel, Field, ConfigDict


class AuthorNestedSchema(BaseModel):
    name: str
    bio: str


class BookReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    summary: str
    publication_date: datetime.date
    author: AuthorNestedSchema


class BookCreateSchema(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date
    author_id: int


class BookNestedSchema(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date


class AuthorReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    bio: str
    books: list[BookNestedSchema]


class AuthorCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    bio: str
