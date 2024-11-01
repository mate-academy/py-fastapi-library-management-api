from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base


class Author(Base):
    __tablename__ = "Author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    bio = Column(String(255))
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "Book"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    summary = Column(String)
    publication_date = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey("Author.id"))

    author = relationship("Author", back_populates="books")
