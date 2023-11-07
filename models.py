from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import BaseModel


class Author(BaseModel):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(63), unique=True, nullable=True)
    bio = Column(String(255), nullable=True)
    books = relationship("Book", back_populates="author")


class Book(BaseModel):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(63), unique=True, nullable=True)
    summary = Column(String(255), nullable=True)
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("Author", back_populates="books")
