from datetime import date

from pydantic import BaseModel

class AuthorBase(BaseModel):
    name:str
    bio:str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class AuthorUpdate(BaseModel):
    name: str | None
    bio: str | None
    

class Book(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int

class BookCreate(Book):
    id: int

    class Config:
        orm_mode = True

class BookUpdate(BaseModel):
    title: str | None = None
    summary: str | None = None
    publication_date: date | None = None
    author_id: int | None = None