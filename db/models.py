from db.database import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    bio = Column(String(511), nullable=False)
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(511), nullable=False)
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    author = relationship("Author", back_populates="books")
