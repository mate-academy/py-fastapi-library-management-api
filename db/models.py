import datetime

from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.engine import Base

class Author(Base):
    __tablename__ = "author"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    bio: Mapped[str] = mapped_column(String(255))
    books: Mapped[list["Book"]] = relationship(back_populates="author")

class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(String(255))
    publication_date: Mapped[datetime.date] = mapped_column(Date)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped["Author"] = relationship(back_populates="books")
