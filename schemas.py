from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    ...


class AuthorUpdate(AuthorBase):
    ...


class AuthorRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str
    summary: str


class BookCreate(BookBase):
    author_id: int


class BookUpdate(BookBase):
    ...


class BookRead(BookBase):
    id: int
    author: AuthorRead

    model_config = ConfigDict(from_attributes=True)
