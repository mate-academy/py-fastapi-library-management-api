import datetime

from pydantic import BaseModel, ConfigDict, Field


class BookBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    summary: str
    publication_date: datetime.date


class BookCreateSchema(BookBaseSchema):
    author_id: int


class BookReadSchema(BookBaseSchema):
    id: int
    author_id: int


class AuthorBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    bio: str


class AuthorCreateSchema(AuthorBaseSchema):
    pass


class AuthorReadSchema(AuthorBaseSchema):
    id: int


class AuthorDetailSchema(AuthorBaseSchema):
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
    id: int
    author: AuthorReadSchema | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 21,
                "title": "Harry Potter",
                "summary": "Phylosopher Stone",
                "publication_date": "2025-05-29",
                "author": {"id": 2, "name": "Joan Roaling", "bio": "Best writer"},
            }
        }
    )


AuthorReadSchema.model_rebuild()
AuthorDetailSchema.model_rebuild()
BookDetailSchema.model_rebuild()
