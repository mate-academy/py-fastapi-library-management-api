from datetime import date

from sqlalchemy import Date, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Author(Base):
    """
    Author model representing a book author in the library system.

    Attributes:
        id (int): Unique identifier for the author.
        name (str): Author's full name, limited to 100 characters. Must be unique.
        bio (str): Author's biography or description, limited to 1000 characters.
        books (list[Book]): List of books written by this author.
    """

    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    bio: Mapped[str] = mapped_column(String(1000))

    books: Mapped[list["Book"]] = relationship(back_populates="author")

    def __repr__(self) -> str:
        return f"Author(id={self.id}, name={self.name})"


class Book(Base):
    """
    Book model representing a book in the library system.

    Attributes:
        id (int): Unique identifier for the book.
        title (str): Book title, limited to 200 characters.
        summary (str): Book summary or description, limited to 2000 characters.
        publication_date (date): Date when the book was published.
        author_id (int): Foreign key reference to the author's ID.
        author (Author): Reference to the author object.

    Notes:
        The model enforces unique constraint for:
        - Combination of title and author_id.
    """

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    summary: Mapped[str] = mapped_column(String(2000))
    publication_date: Mapped[date] = mapped_column(Date)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    author: Mapped["Author"] = relationship(back_populates="books")

    __table_args__ = (
        UniqueConstraint("title", "author_id", name="unique_title_author"),
    )

    def __repr__(self) -> str:
        return f"Book(id={self.id}, title={self.title}, author_id={self.author_id})"
