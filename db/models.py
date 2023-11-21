from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from db.engine import Base


class DBBook(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    summary = Column(String(1000))
    publication_date = Column(Date)
    author = relationship("DBAuthor", back_populates="books")
    author_id = Column(Integer, ForeignKey("authors.id"))


class DBAuthor(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    bio = Column(String(1000))
    books = relationship("DBBook", back_populates="author")
