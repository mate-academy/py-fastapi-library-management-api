from sqlalchemy import ForeignKey, String, Date
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    bio: Mapped[str] = mapped_column(String, nullable=True)

    books: Mapped[list["Book"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    summary: Mapped[str] = mapped_column(String, nullable=True)
    publication_date: Mapped[Date] = mapped_column(Date, nullable=False)

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id", ondelete="CASCADE"), nullable=False
    )
    author: Mapped["Author"] = relationship(back_populates="books")
