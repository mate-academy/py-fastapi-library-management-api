"""Pydantic schemas for authors and books."""

import datetime

from pydantic import BaseModel, ConfigDict, Field


class BookBaseSchema(BaseModel):
    """Base schema for book."""

    model_config = ConfigDict(from_attributes=True)

    title: str
    summary: str
    publication_date: datetime.date


class BookCreateSchema(BookBaseSchema):
    """Schema for creating a book."""

    author_id: int


class BookReadSchema(BookBaseSchema):
    """Schema for reading a book."""

    id: int
    author_id: int


class AuthorBaseSchema(BaseModel):
    """Base schema for author."""

    model_config = ConfigDict(from_attributes=True)

    name: str
    bio: str


class AuthorCreateSchema(AuthorBaseSchema):
    """Schema for creating an author."""

    pass


class AuthorReadSchema(AuthorBaseSchema):
    """Schema for reading an author."""

    id: int


class AuthorDetailSchema(AuthorBaseSchema):
    """Detailed schema for author with books."""

    id: int
    books: list[BookReadSchema] = Field(default_factory=list)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 2,
                "name": "Joan Roaling",
                "bio": "Best writer",
                "books": [
                    {
                        "id": 21,
                        "title": "Harry Potter",
                        "summary": "Phylosopher Stone",
                        "publication_date": "2025-05-29",
                        "author_id": 2,
                    }
                ],
            }
        }
    )


class BookDetailSchema(BookBaseSchema):
    """Detailed schema for book with author."""

    id: int
    author: AuthorReadSchema | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 21,
                "title": "Harry Potter",
                "summary": "Phylosopher Stone",
                "publication_date": "2025-05-29",
                "author": {
                    "id": 2,
                    "name": "Joan Roaling",
                    "bio": "Best writer",
                },
            }
        }
    )


AuthorReadSchema.model_rebuild()
AuthorDetailSchema.model_rebuild()
BookDetailSchema.model_rebuild()
