from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base


# Author model
class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    bio = Column(String(255), nullable=False)

    # Relationship with Book (One-to-Many)
    books = relationship("Book", back_populates="author")


# Book model
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(255), nullable=False)
    publication_date = Column(Date(), nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"))

    # Relationship with Author (Many-to-One)
    author = relationship("Author", back_populates="books")
