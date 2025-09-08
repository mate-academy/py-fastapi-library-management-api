from pydantic import BaseModel
from datetime import date
from typing import Optional


class AuthorBaseSchema(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreateSchema(AuthorBaseSchema):
    pass


class AuthorSchema(AuthorBaseSchema):
    id: int

    class Config:
        orm_mode = True


class BookBaseSchema(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: date


class BookCreateSchema(BookBaseSchema):
    pass


class BookSchema(BookBaseSchema):
    id: int

    class Config:
        orm_mode = True
