from datetime import date

from pydantic import BaseModel, ConfigDict


class AuthorCreate(BaseModel):
    name: str
    bio: str


class AuthorRead(BaseModel):
    id: int
    name: str
    bio: str

    model_config = ConfigDict(from_attributes=True)


class BookCreate(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookRead(BookCreate):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)
