from pydantic import BaseModel
from datetime import date

class AuthorBase(BaseModel):
    name: str
    bio: str

class CreateAuthor(AuthorBase):
    pass


class Author(AuthorBase):
    id: int


    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int

class CreateBook(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True
