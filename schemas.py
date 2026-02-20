from datetime import date
from typing import Optional

from pydantic import BaseModel


#Author_data_model___________________________________________________________________
class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] | None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        model_config = {"from_attributes": True}


#Book_data_model_______________________________________________________________________

class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: Optional[date] | None

class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author: Author

    class Config:
        model_config = {"from_attributes": True}
