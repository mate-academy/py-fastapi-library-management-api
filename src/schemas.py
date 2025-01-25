import datetime

from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreateResponseSchema(AuthorBase):
    pass


class AuthorResponseSchema(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date
    author_id: int


class BookCreateResponseSchema(BookBase):
    pass


class BookResponseSchema(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
