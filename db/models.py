import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from db.database import Base


class DBAuthor(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)
    bio: Mapped[str] = mapped_column()

    books: Mapped[list["DBBook"]] = relationship(back_populates="author")


class DBBook(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column()
    summary: Mapped[str] = mapped_column()
    publication_date: Mapped[datetime.date] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    author: Mapped["DBAuthor"] = relationship(back_populates="books")
