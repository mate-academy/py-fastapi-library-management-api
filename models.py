from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(555), nullable=False)
    publication_date = Column(Date, nullable=True)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship("Author", back_populates="books")


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    bio = Column(String(555), nullable=False)
    books = relationship("Book", back_populates="author")
