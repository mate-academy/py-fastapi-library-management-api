from datetime import date

from pydantic import BaseModel, field_validator


class BookBase(BaseModel):
    title: str
    summary: str | None = None
    publication_date: date
    author_id: int


class BookCreate(BookBase):
    @field_validator("publication_date")
    def validate_publication_date(cls, value: date) -> date:
        today = date.today()
        if value > today:
            raise ValueError("Publication date cannot be in the future")
        return value


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[Book] = []

    class Config:
        orm_mode = True
