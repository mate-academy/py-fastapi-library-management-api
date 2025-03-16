import datetime

from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, ForeignKey


class AuthorModel(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    bio: Mapped[str] = mapped_column(String(255), nullable=False)

    books: Mapped[list["BookModel"]] = relationship(
        "BookModel",
        back_populates="author"
    )


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    summary: Mapped[str] = mapped_column(String(255), nullable=False)
    publication_date: Mapped[datetime.date] = mapped_column(
        Date,
        nullable=False
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id"),
        nullable=False
    )
    author: Mapped["AuthorModel"] = relationship(
        "AuthorModel",
        back_populates="books"
    )
