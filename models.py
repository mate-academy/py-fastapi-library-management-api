from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    bio = Column(String(250))

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    summary = Column(String(250), index=True)
    publication_date = Column(DateTime)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship("Author", back_populates="books")
