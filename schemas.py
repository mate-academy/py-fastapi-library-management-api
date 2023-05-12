from pydantic import BaseModel, validator, EmailStr
from datetime import date, datetime


class BookBase(BaseModel):
    title: str
    summary: str | None = None
    publication_date: date

    @validator("publication_date")
    def validate_date(cls, value):
        print(value)
        if value > datetime.now().date():
            raise ValueError("Date cannot be in future")
        return value


class BookShort(BaseModel):
    title: str
    publication_date: date

    class Config:
        orm_mode = True


class BookCreate(BookBase):
    author_id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorShort(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Book(BookBase):
    id: int
    author: AuthorShort | None = None

    class Config:
        orm_mode = True


class AuthorCreate(AuthorBase):

    class Config:
        orm_mode = True


class Author(AuthorBase):
    id: int
    books: list[BookShort] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    date_created: datetime

    class Config:
        orm_mode = True
