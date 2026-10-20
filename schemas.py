from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int
    books: list["BookRead"] = []

    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str
    summary: str


class BookCreate(BookBase):
    author_id: int


class BookAuthorRead(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BookRead(BookBase):
    id: int
    author: BookAuthorRead

    model_config = ConfigDict(from_attributes=True)
