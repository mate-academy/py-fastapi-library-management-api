from pydantic import BaseModel
from datetime import datetime


class AuthorSchemaBase(BaseModel):
    name: str
    bio: str

    class Config:
        from_attributes = True


class AuthorCreateSchema(AuthorSchemaBase):
    pass


class AuthorSchema(AuthorSchemaBase):
    id: int

    class Config:
        from_attributes = True


class BookSchemaBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime
    author_id: int


class BookCreateSchema(BookSchemaBase):
    pass


class BookSchema(BookSchemaBase):
    id: int

    class Config:
        from_attributes = True
