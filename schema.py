from pydantic import BaseModel

class BaseAuthor(BaseModel):
    name: str
    bio: str

class AuthorCreate(BaseAuthor):
    pass


class Author(BaseModel):
    id: int

    class Config:
        orm_mode = True

class BaseBook(BaseModel):
    title: str
    author: Author
    summary: str


class BookCreate(BaseBook):
    pass


class Book(BaseModel):
    id: int


    class Config:
        orm_mode = True

