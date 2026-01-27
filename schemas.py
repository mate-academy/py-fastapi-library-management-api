import datetime

from sqlmodel import SQLModel


class AuthorUpdate(SQLModel):
    name: str
    bio: str | None
    books: int | None


class AuthorCreate(SQLModel):
    name: str
    bio: str | None
    books: int | None


class BookUpdate(SQLModel):
    title: str
    summary: str | None
    publication_date: datetime.date | None
    author_id: int


class BookCreate(SQLModel):
    title: str
    summary: str
    publication_date: datetime.date
    author_id: int
