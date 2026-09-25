from datetime import date

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str | None
    model_config = ConfigDict(from_attributes=True)


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int
    model_config = ConfigDict(from_attributes=True)


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    id: int