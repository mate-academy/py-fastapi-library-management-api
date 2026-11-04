from pydantic import BaseModel, ConfigDict
import datetime


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorResponse(AuthorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str
    publication_date: datetime.date
    summary: str


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
