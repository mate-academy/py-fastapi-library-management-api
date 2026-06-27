from datetime import datetime
from pydantic import BaseModel, ConfigDict



class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(BaseModel):
    id: int
    books: "BookBase"

    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime

class BookCreate(BookBase):
    id: int
    author_id: int


class Book(BookBase):
    id: int
    author: "AuthorBase"
