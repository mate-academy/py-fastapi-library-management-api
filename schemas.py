from datetime import date
from typing import List

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str

class AuthorCreate(AuthorBase):
    pass

class NumOfAuthor(AuthorBase):
    id: int
    class Config:
        from_attributes = True

class AuthorList(BaseModel):
    authors: List[AuthorBase]

class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date

class BookCreate(BookBase):
    pass

class NumOfBook(BookBase):
    id: int
    author: NumOfAuthor
    class Config:
        from_attributes = True

class BookList(BaseModel):
    books: List[BookBase]