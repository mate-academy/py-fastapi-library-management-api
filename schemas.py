from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(max_length=60)
    summary: str = Field(max_length=150)
    publication_date: date | None = None


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorBase(BaseModel):
    name: str = Field(max_length=30)
    bio: str = Field(max_length=150)


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorWithBooks(AuthorRead):
    books: list[BookRead] = Field(default_factory=list)
