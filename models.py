from datetime import date

from sqlmodel import Field, SQLModel, Relationship

from database import create_db_and_tables


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True, unique=True)
    summary: str | None
    publication_date: date | None
    author_id: int = Field(default=None, foreign_key="author.id")


class Author(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    bio: str | None
    books: Book | None = Relationship(back_populates="author")


#run once to create db
if __name__ == "__main__":
    create_db_and_tables()
