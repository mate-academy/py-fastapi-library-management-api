from datetime import date

from pydantic import BaseModel
from pydantic import ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date
    author: Author

class BookCreate(BookBase):
    title: str
    summary: str
    author_id: int
    publication_date: date

class Book(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
