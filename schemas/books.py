from datetime import date

from pydantic import BaseModel


class BookCreateSchema(BaseModel):
    title: str
    summary: str | None
    publication_date: date | None
    author_id: int | None


class BookResponseSchema(BookCreateSchema):
    id: int

    model_config = {"from_attributes": True}


class BookListSchema(BaseModel):
    books: list[BookResponseSchema]

    model_config = {"from_attributes": True}
