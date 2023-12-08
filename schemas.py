from pydantic import BaseModel

import models


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[models.Book] = []

    class Config:
        orm_mode = True

