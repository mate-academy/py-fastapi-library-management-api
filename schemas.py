import datetime
from pydantic import BaseModel


class BookSchemaBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date
    author_id: int

    class Config:
        from_attributes = True


class BookCreateSchema(BookSchemaBase):
    pass


class BookListSchema(BookSchemaBase):
    id: int


class AuthorSchemaBase(BaseModel):
    name: str
    bio: str

    class Config:
        from_attributes = True


class AuthorSchema(AuthorSchemaBase):
    id: int

    class Config:
        from_attributes = True


class AuthorListSchema(AuthorSchemaBase):
    id: int
    books: list[BookListSchema] = []
