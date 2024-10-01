from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    bio = Column(String)
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    summary = Column(String)
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("Author", back_populates="books")
