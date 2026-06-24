from datetime import date

from pydantic import BaseModel, Field

try:
    from pydantic import ConfigDict
except ImportError:
    ConfigDict = None


if ConfigDict is not None:

    class OrmBaseModel(BaseModel):
        model_config = ConfigDict(from_attributes=True)

else:

    class OrmBaseModel(BaseModel):
        class Config:
            orm_mode = True


class BookBase(OrmBaseModel):
    title: str
    summary: str | None = None
    publication_date: date


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int


class AuthorBase(OrmBaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[Book] = Field(default_factory=list)
