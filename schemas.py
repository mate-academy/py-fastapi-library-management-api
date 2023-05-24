from datetime import datetime


from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class Authors(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class CreateAuthor(AuthorBase):
    pass


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime


class Books(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class CreateBook(BookBase):
    pass
