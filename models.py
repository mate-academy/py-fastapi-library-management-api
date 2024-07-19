from __future__ import annotations

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, Date, ForeignKey

from database import Base


class DBAuthor(Base):
    __tablename__ = 'author'
    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String(255), nullable=False, unique=True)
    bio = mapped_column(String(500), nullable=False)
    books: Mapped[list["DBBook"]] = relationship(
        "DBBook",
        back_populates="author",
        cascade="all, delete",
    )

    def __repr__(self) -> str:
        return f"Author(name={self.name})"


class DBBook(Base):
    __tablename__ = 'book'

    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String(255), nullable=False)
    summary = mapped_column(String(500), nullable=False)
    publication_date = mapped_column(Date, nullable=False)
    author_id = mapped_column(ForeignKey('author.id'), nullable=False)
    author: Mapped[DBAuthor] = relationship(
            "DBAuthor",
            back_populates="books",
        )