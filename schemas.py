from pydantic import BaseModel
from typing import List


# Book schemas
class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: str
    

class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


# Author schemas
class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[Book]

    class Config:
        orm_mode = True
