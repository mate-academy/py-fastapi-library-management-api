from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    bio = Column(String, nullable=True)

    # Relationship to books. cascade delete ensures books are removed if an author is deleted.
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary key=True, index=True)
    title = Column(String, index=True, nullable=False)
    summary = Column(String, nullable=True)
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    # Relationship back to author
    author = relationship("Author", back_populates="books")
