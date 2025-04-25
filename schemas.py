from datetime import date

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorSchema(AuthorBase):  # Renamed to avoid conflict
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class BookSchema(BookBase):  # Renamed to avoid conflict
    id: int
    author: AuthorSchema

    class Config:
        orm_mode = True
