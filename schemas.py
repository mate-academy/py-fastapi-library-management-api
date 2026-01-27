from pydantic import BaseModel

from models import Book


class AuthorBase(BaseModel):
    id: int
    name: str
    bio: str
    books: Book


class AuthorRead(AuthorBase):
    pass
