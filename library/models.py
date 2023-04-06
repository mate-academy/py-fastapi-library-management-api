from sqlalchemy import Column, Integer, String, Date, ForeignKey

from sqlalchemy.orm import relationship

from library.engine import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    bio = Column(String(255), nullable=False, unique=True)

    books = relationship("Book", back_populates="authors")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True)
    summary = Column(String(255))
    publication_date = Column(Date)
    authot_id = Column(Integer, ForeignKey("author.id"))

    authors = relationship("Author", back_populates="books")