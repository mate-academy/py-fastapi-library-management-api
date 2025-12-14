from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    bio = Column(String, nullable=True)

    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    summary = Column(String, nullable=True)
    publication_date = Column(Date, nullable=True)

    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False, index=True)
    author = relationship("Author", back_populates="books")
