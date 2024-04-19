from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(63), nullable=False)
    summary = Column(String(255), nullable=False)
    publication_date = Column(DateTime, )
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("Author", back_populates="book")

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(63), nullable=False, unique=True)
    bio = Column(String(255), nullable=False)

    book = relationship("Book", back_populates="author")
