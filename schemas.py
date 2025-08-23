from datetime import date

from pydantic import BaseModel


class BookBaseSchema(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookSchema(BookBaseSchema):
    id: int

    class Config:
        orm_mode = True


class BookCreateSchema(BookBaseSchema):
    pass


class AuthorBaseSchema(BaseModel):
    name: str
    bio: str


class AuthorSchema(AuthorBaseSchema):
    id: int

    class Config:
        orm_mode = True


class AuthorCreateSchema(AuthorBaseSchema):
    pass
