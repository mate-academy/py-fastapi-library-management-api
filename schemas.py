from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorName(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author: AuthorName

    class Config:
        orm_mode = True
