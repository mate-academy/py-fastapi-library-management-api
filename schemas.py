import datetime

from pydantic import BaseModel, validator

from models import Book, Author


class AuthorBase(BaseModel):
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorMain(AuthorBase):
    id: int
    books: list[Book] = []

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    summary: str = None
    publication_date: datetime.date = datetime.date.today()


class BookCreate(BookBase):
    author_ids: list[int] = []

    @validator("author_ids")
    def validate_author_ids(self, author_ids, *, values):
        existing_author_ids = {author.id for author in values.get("authors", [])}
        for author_id in author_ids:
            if author_id not in existing_author_ids:
                raise ValueError(f"Author with ID {author_id} doesn't exist")
        return author_ids


class BookMain(BookBase):
    id: str
    authors: list[Author]

    class Config:
        orm_mode = True
