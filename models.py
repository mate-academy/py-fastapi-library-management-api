from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    bio = Column(String(500))
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    summary = Column(String(500))
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship('Author', back_populates='books')
