from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from database import Base


class DBAuthor(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(225), nullable=False, unique=True)
    bio = Column(String(1023))

    books = relationship("DBBook", back_populates="author")


class DBBook(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(127), nullable=False)
    summary = Column(String(511))
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("DBAuthor", back_populates="books")
