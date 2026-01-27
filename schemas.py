from datetime import date
from typing import List, Optional

from pydantic import BaseModel


try:
    from pydantic import ConfigDict  # pydantic v2

    class _ORMBase(BaseModel):
        model_config = ConfigDict(from_attributes=True)
except Exception:  # pydantic v1
    class _ORMBase(BaseModel):
        class Config:
            orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: date


class BookCreateSchema(BookBase):
    pass


class BookSchema(_ORMBase, BookBase):
    id: int
    author_id: int


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreateSchema(AuthorBase):
    pass


class AuthorSchema(_ORMBase, AuthorBase):
    id: int
    books: List[BookSchema] = []
