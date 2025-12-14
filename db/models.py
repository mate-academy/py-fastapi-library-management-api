import datetime
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(251), unique=True, nullable=False)
    bio: Mapped[str] = mapped_column(String(500), nullable=False)
    books: Mapped[list["DBBook"]] = relationship(back_populates="author")


class DBBook(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(251), nullable=False)
    summary: Mapped[str] = mapped_column(String(500), nullable=False)
    publication_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped["DBAuthor"] = relationship(back_populates="books")
