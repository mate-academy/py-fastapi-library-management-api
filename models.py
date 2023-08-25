from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(127), unique=True)
    bio = Column(String(511))

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    summary = Column(String)
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("Author", back_populates="books")
