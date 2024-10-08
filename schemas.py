from pydantic import BaseModel
from datetime import date


class Author(BaseModel):
    id: int
    name: str
    bio: str


class Book(BaseModel):
    id: int
    title: str
    summary: str
    publication_date: date
    author_id: int


class CreateAuthor(BaseModel):
    name: str
    bio: str


class CreateBook(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int
