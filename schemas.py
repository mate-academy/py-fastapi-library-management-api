from pydantic import BaseModel
from datetime import date
from pydantic import Field

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    skip: int = Field(0, ge=0)

class AuthorBase(BaseModel):
    name: str
    bio: str

class AuthorRead(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class AuthorCreate(AuthorBase):
    pass



class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: date

class BookRead(BookBase):
    id: int
    author_id: int
    class Config:
        from_attributes = True

class BookCreate(BookBase):
    author_id: int
