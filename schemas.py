from datetime import date

from pydantic import BaseModel


class AuthorBaseSchema(BaseModel):
    name: str
    bio: str


class AuthorSchema(AuthorBaseSchema):
    id: int

    class Config:
        from_attributes = True


class PaginatedAuthorsSchema(BaseModel):
    items: list[AuthorSchema]
    total: int
    skip: int
    limit: int


class AuthorCreateSchema(AuthorBaseSchema):
    pass


class BookBaseSchema(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookSchema(BookBaseSchema):
    id: int
    author: AuthorSchema

    class Config:
        from_attributes = True


class PaginatedBooksSchema(BaseModel):
    items: list[BookSchema]
    total: int
    skip: int
    limit: int


class BookCreateSchema(BookBaseSchema):
    author_id: int
    pass
