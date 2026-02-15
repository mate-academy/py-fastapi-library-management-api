from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    summary: str = Field(..., min_length=1)
    publication_date: date | None = None


class BookCreate(BookBase):
    pass


class BookOut(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int


class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1)
    bio: str = Field(..., min_length=1)


class AuthorCreate(AuthorBase):
    pass


class AuthorOut(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    books: list[BookOut] = Field(default_factory=list)
