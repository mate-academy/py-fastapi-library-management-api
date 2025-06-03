"""ORM models for authors and books."""

from datetime import datetime

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base declarative class."""

    @classmethod
    def default_order_by(cls) -> None:
        """Default order by for models."""
        return None


class DbAuthor(Base):
    """Author model."""

    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    bio: Mapped[str] = mapped_column(String(255))
    books = relationship("DbBook", back_populates="author")


class DbBook(Base):
    """Book model."""

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), unique=True)
    summary: Mapped[str] = mapped_column(String(255))
    publication_date: Mapped[datetime.date] = mapped_column(
        Date, nullable=False
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id"), nullable=False
    )

    author = relationship("DbAuthor", back_populates="books")
