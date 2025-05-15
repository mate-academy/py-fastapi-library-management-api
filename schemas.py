from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel, Field, field_validator


class AuthorBaseSchema(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreateSchema(AuthorBaseSchema):
    pass


class BookBaseSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    summary: Optional[str] = Field(None, max_length=511)
    published_date: date = Field(
        ...,
        description="The publication date of the book "
        "in ISO format (YYYY-MM-DD)"
    )

    @field_validator("published_date", mode="before")
    @classmethod
    def validate_published_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(
                    "Invalid date format for 'published_date'. "
                    "Expected format: YYYY-MM-DD."
                )
        elif isinstance(value, date):
            return value
        raise ValueError(
            "Invalid type for 'published_date'. "
            "Must be a string in YYYY-MM-DD format or a date object."
        )


class BookCreateSchema(BookBaseSchema):
    author_id: int


class BookSchema(BookBaseSchema):
    id: int
    author: AuthorBaseSchema

    class Config:
        orm_mode = True


class PaginatedBooksSchema(BaseModel):
    total: int
    page: int
    per_page: int
    books: List[BookSchema]

    class Config:
        orm_mode = True


class PaginatedAuthorsSchema(BaseModel):
    total: int
    page: int
    per_page: int
    authors: List[AuthorBaseSchema]

    class Config:
        orm_mode = True
