import datetime

from sqlalchemy import String, Date, func, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from database import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )
    bio: Mapped[str] = mapped_column(String(255), nullable=True)

    books: Mapped[list["Book"]] = relationship(
        back_populates="author", lazy="selectin"
    )


class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(
        String(255), nullable=False,
    )
    summary: Mapped[str] = mapped_column(String(255), nullable=True)
    publication_date: Mapped[datetime.date] = mapped_column(
        Date, server_default=func.current_date()
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    author: Mapped["Author"] = relationship(back_populates="books")

