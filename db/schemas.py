from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class AuthorBase(BaseModel):
    name: str
    bio: str


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime


class AuthorCreate(AuthorBase):
    pass


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class Author(AuthorBase):
    id: int
    books: list[Book] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
