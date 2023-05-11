from datetime import date

from pydantic import BaseModel


import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class BookBase(BaseModel):
    title: str
    summary: str = None
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str
    bio: str = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    name: str = None


class Author(AuthorBase):
    id: int
    books: list[Book] = []

    class Config:
        orm_mode = True
