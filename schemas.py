from datetime import date

from pydantic import BaseModel, Field


class AuthorBase(BaseModel):
    name: str = Field(..., max_length=255)
    bio: str | None = Field(None, max_length=511)


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list["BookNested"] = []

    class Config:
        from_attributes = True


class AuthorNested(BaseModel):
    name: str = Field(..., max_length=255)
    id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str = Field(..., max_length=255)
    summary: str = Field(..., max_length=511)
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author: AuthorNested

    class Config:
        from_attributes = True


class BookNested(BookBase):
    id: int

    class Config:
        from_attributes = True
