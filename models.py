from database import Base

from sqlalchemy import Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Author(Base):
    __tablename__ = 'author'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    bio: Mapped[str] = mapped_column(String(511), nullable=True)
    books: Mapped[list["Book"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )


class Book(Base):
    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(String(511), nullable=True)
    publication_date: Mapped[Date] = mapped_column(Date, nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"), nullable=False)

    author: Mapped["Author"] = relationship(back_populates="books")
