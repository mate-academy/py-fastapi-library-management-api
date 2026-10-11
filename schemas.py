from pydantic import BaseModel, ConfigDict
import datetime


class BookBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    summary: str | None = None
    publication_date: datetime.date

class AddBook(BookBase):
    author_id: int

class BookResponse(BookBase):
    id: int
    author_id: int

class AuthorBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    bio: str

class AddAuthor(AuthorBase):
    pass

class AuthorResponse(AuthorBase):
    id: int