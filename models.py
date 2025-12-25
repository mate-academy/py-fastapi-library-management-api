from datetime import date

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    bio: Mapped[str] = mapped_column(String(255), nullable=True)

    books: Mapped["Book"] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    summary: Mapped[str] = mapped_column(String(512), nullable=True)
    publication_date: Mapped[date] = mapped_column(nullable=False)

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id",)
    )

    author: Mapped["Author"] = relationship(back_populates="books")
