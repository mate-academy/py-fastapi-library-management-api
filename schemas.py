from pydantic import BaseModel
from datetime import date


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class AuthorPartialUpdate(BaseModel):
    name: str = None
    bio: str = None


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author: Author

    class Config:
        orm_mode = True


class BookPartialUpdate(BaseModel):
    title: str = None
    summary: str = None
    publication_date: date = None
    author_id: int = None


class UserAuth(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    is_active: bool

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str
    exp: int


class SystemUser(UserOut):
    pass
