from datetime import date, datetime
from typing import List, Optional, Generic, TypeVar

from pydantic import BaseModel, field_validator, Field, ConfigDict


T = TypeVar("T")


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    summary: str = Field(..., min_length=1, max_length=511)
    publication_date: date = Field(
        ...,
        description="The publication date of the book "
        "in ISO format (YYYY-MM-DD)"
    )

    @field_validator("publication_date", mode="before")
    @classmethod
    def validate_publication_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(
                    "Invalid date format for 'publication_date'. "
                    "Expected format: YYYY-MM-DD."
                )
        elif isinstance(value, date):
            return value
        raise ValueError(
            "Invalid type for 'publication_date'. "
            "Must be a string in YYYY-MM-DD format or a date object."
        )

    model_config = ConfigDict(from_attributes=True)


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author: Author

    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    skip: int
    limit: int


class PaginatedAuthors(PaginatedResponse[Author]):
    pass


class PaginatedBooks(PaginatedResponse[Book]):
    pass
