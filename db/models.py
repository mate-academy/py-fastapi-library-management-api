from sqlalchemy import Column, Integer, String, Date, ForeignKey

from sqlalchemy.orm import relationship

from db.database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100),  nullable=False, unique=True, index=True)
    bio = Column(String(500),  nullable=False)
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100),  nullable=False)
    summary = Column(String(500),  nullable=False)
    publication_date = Column(Date,  nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")
