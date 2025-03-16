from datetime import date

from pydantic import BaseModel

from db.models import Author


class BookSchemaBase(BaseModel):
    title: str
    summary: str
    publication_date: date


class BookSchemaCreate(BookSchemaBase):
    author_id: int


class BookSchemaResponse(BookSchemaBase):
    id: int
    author: Author

    class Config:
        orm_mode = True


class AuthorSchemaBase(BaseModel):
    name: str
    bio: str


class AuthorSchemaCreate(AuthorSchemaBase):
    pass


class AuthorSchemaResponse(AuthorSchemaBase):
    id: int

    class Config:
        from_attributes = True
