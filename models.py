from sqlalchemy import Column
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.types import Date
from database import engine
from datetime import date


class DBAuthor(SQLModel, table=True):
    __tablename__ = 'author'

    id: int = Field(primary_key=True)
    name: str = Field(unique=True)
    bio: str = Field()
    books: list['DBBook'] = Relationship(back_populates='author')


class DBBook(SQLModel, table=True):
    __tablename__ = 'book'

    id: int | None = Field(default=None, primary_key=True)
    title: str | None = Field(default=None)
    summary: str | None = Field(default=None)
    publication_date: date = Field(sa_column=Column(Date, nullable=False))

    author_id: int | None = Field(default=None, foreign_key='author.id')
    author: DBAuthor | None = Relationship(back_populates='books')


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
