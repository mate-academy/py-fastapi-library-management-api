import datetime

from sqlalchemy import Integer, Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db.engine import Base


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True, unique=True)
    bio = Column(String(1023), nullable=True)
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=True, unique=True)
    summary = Column(String(1023), nullable=True)
    publication_date = Column(DateTime, default=datetime.datetime.utcnow)
    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship("Author", back_populates="books")
