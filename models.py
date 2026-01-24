from datetime import datetime, date

from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    bio: Mapped[str] = mapped_column(String(), index=True)
    books: Mapped[list["DBBook"]] = relationship(
        back_populates="author"
    )


class DBBook(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    summary: Mapped[str] = mapped_column(String(), index=True)
    publication_date: Mapped[date] = mapped_column(Date, index=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("author.id")
    )
    author: Mapped[DBAuthor] = relationship(
        back_populates="books"
    )
