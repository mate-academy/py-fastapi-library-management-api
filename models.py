from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import mapped_column, relationship

from database import Base


class Author(Base):
    __tablename__ = "author"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, unique=True)
    bio = mapped_column(String(255))
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "book"
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String)
    summary = mapped_column(String(255))
    publication_date = mapped_column(Date)
    author_id = mapped_column(ForeignKey("author.id"))
    author = relationship("Author", back_populates="books")
