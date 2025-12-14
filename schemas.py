from datetime import date
from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    summary: str | None = None
    publication_date: date | None = None


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    author_id: int


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    books: list[BookRead] = []
