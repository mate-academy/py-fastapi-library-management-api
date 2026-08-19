from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from library_api.database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    bio = Column(String, nullable=True)

    # Relationship back-reference to automatically pull associated books
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    summary = Column(String, nullable=True)
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    # Relationship links back to the parent Author object
    author = relationship("Author", back_populates="books")
