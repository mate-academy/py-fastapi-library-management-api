from datetime import date

from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base



# class Author(Base):
#     __tablename__ = "author"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255), nullable=False, unique=True)
#     bio = Column(String(255), nullable=False)
#     books = Column(Integer, One)
#
#
# class Book(Base):
#     __tablename__ = "book"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(255), nullable=False)
#     summary = Column(String(255), nullable=False)
#     publication_date = Column(Date, nullable=False)
#     author_id = Column(Integer, ForeignKey("author.id"))


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    bio: Mapped[str] = mapped_column(String(255), nullable=False)
    books: Mapped[list["Book"]] = relationship(
        back_populates="author"
    )


class Book(Base):

    __tablename__ = "book"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(String(255), nullable=False)
    publication_date: Mapped[date] = mapped_column(Date, nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("author.id"), nullable=False
    )
    author: Mapped["Author"] = relationship(
        back_populates="books"
    )
