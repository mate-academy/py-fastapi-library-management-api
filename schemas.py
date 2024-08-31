import datetime

from pydantic import BaseModel


class AuthorSchema(BaseModel):
    name: str
    bio: str


class AuthorSchemaCreate(AuthorSchema):
    pass


class BookSchema(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date
    author_id: int


class BookSchemaList(BookSchema):
    id: int
    author: AuthorSchema

    class Config:
        orm_mode = True


class AuthorSchemaList(AuthorSchema):
    id: int
    books: list[BookSchemaList]

    class Config:
        orm_mode = True


class BookSchemaCreate(BookSchema):
    pass
