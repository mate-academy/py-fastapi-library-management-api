from pydantic import BaseModel, ConfigDict
from datetime import date


class AuthorCreate(BaseModel):
    name: str
    bio: str


class Author(AuthorCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BookCreate(BaseModel):
    title: str
    summary: str
    publication_date: date


class Book(BookCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

