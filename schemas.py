from datetime import date

from pydantic import BaseModel, ConfigDict


class AuthorCreate(BaseModel):
    name: str
    bio: str


class Author(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    bio: str


class BookCreate(BaseModel):
    title: str
    summary: str
    publication_date: date


class Book(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    summary: str
    publication_date: date
    author_id: int
