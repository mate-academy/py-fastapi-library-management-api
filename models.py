from datetime import date

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Author(Base):
    __tablename__ = "author"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(255), unique=True, nullable=False)
    bio: str = Column(String(5000))
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "book"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(255), nullable=False)
    summary: str = Column(String(2000), nullable=False)
    publication_date: date = Column(Date, nullable=False)
    author_id: int = Column(Integer, ForeignKey("author.id"))

    author = relationship("Author", back_populates="books")
