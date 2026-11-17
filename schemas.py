import datetime

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    name: str | None = None


class AuthorRead(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str
    summary: str | None = None


class BookCreate(BookBase):
    author_id: int
    publication_date: datetime.date


class BookUpdate(BookBase):
    title: str | None = None
    author_id: int | None = None
    publication_date: datetime.date | None = None


class BookRead(BookBase):
    id: int
    publication_date: datetime.date
    author: AuthorRead

    model_config = ConfigDict(from_attributes=True)
