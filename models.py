from datetime import date
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    bio: Mapped[str] = mapped_column(String(1000), nullable=True)

    books: Mapped[list["Book"]] = relationship(
        "Book",
        back_populates="author",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(String(2000), nullable=True)
    publication_date: Mapped[date] = mapped_column(Date, nullable=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id"),
        nullable=False
    )

    author: Mapped["Author"] = relationship(
        "Author",
        back_populates="books",
        lazy="selectin"
    )
