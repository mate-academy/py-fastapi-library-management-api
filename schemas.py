from pydantic import BaseModel, ConfigDict
from datetime import date

class AuthorBase(BaseModel):
    name: str
    bio: str

class AuthorRead(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class AuthorCreate(AuthorBase):
    pass



class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date

class BookRead(BookBase):
    id: int
    author_id: int
    class Config:
        orm_mode = True

class BookCreate(BookBase):
    author_id: int