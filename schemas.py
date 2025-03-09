from datetime import date
from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int
    books: list["BookRead"] = []

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    summary: str | None = None
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class BookRead(BookBase):
    id: int
    author: AuthorRead

    class Config:
        from_attributes = True
