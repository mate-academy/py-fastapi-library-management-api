from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, unique=True)
    summary = Column(String(501), nullable=True)
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship("Author", back_populates="books")


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    bio = Column(String(501), nullable=True)

    books = relationship(Book, back_populates="author")
