from datetime import date

from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    bio: Mapped[str | None] = mapped_column(
        String(511),
        nullable=True
    )

    books: Mapped[list["Book"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True
    )

    summary: Mapped[str | None] = mapped_column(
        String(1023),  # Довший опис
        nullable=True
    )

    publication_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id"),
        nullable=False
    )

    author: Mapped["Author"] = relationship(back_populates="books")
