from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Relationship, relationship

from database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    bio = Column(String(511), nullable=True)
    books = Relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(511), nullable=False)
    publication_date = Column(DateTime, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("Author", back_populates="books")
