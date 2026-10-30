from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class BookCreate(BaseModel):
    title: str = Field(max_length=30)
    summary: str = Field(max_length=255)
    publication_date: date
    author_id: int


class BookRead(BaseModel):
    id: int
    title: str
    summary: str
    publication_date: date
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorRead(BaseModel):
    id: int
    name: str
    bio: str
    books: list[BookRead]

    model_config = ConfigDict(from_attributes=True)


class AuthorCreate(BaseModel):
    name: str = Field(max_length=30)
    bio: str = Field(max_length=255)
