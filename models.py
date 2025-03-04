from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column,
                            relationship)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)


class Author(Base):
    __tablename__ = 'author'

    name: Mapped[str] = mapped_column(unique=True)
    bio: Mapped[str] = mapped_column()
    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = 'book'

    title: Mapped[str] = mapped_column(unique=True)
    summary: Mapped[str] = mapped_column()
    publication_date: Mapped[str] = mapped_column(String, default="2000-01-01")

    author_id: Mapped[int] = mapped_column(ForeignKey('author.id'))
    author: Mapped["Author"] = relationship(back_populates="books")
