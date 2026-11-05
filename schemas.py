from datetime import date

from pydantic import BaseModel, ConfigDict


# ---------- Book ----------

class BookBase(BaseModel):
    title: str
    summary: str | None = None
    publication_date: date | None = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = None
    summary: str | None = None
    publication_date: date | None = None
    author_id: int | None = None


class Book(BookBase):
    id: int
    author_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


# ---------- Author ----------

class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: str | None = None
    bio: str | None = None


class Author(AuthorBase):
    id: int
    books: list[Book] = []

    model_config = ConfigDict(from_attributes=True)