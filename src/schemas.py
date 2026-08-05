from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    summary: str


class BookList(BookBase):
    pass


class BookDetail(BookBase):
    author_id: int | None = None


class BookCreate(BookDetail):
    pass


class BookUpdate(BookDetail):
    pass


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorList(AuthorBase):
    pass


class AuthorDetail(AuthorBase):
    books: list[BookBase] | None = None


class AuthorCreate(AuthorDetail):
    books: list[BookBase] | None = None


class AuthorUpdate(AuthorDetail):
    books: list[BookBase] | None = None
