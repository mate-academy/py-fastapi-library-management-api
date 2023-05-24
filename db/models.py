from sqlalchemy import String, Integer, Column, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from db.engine import Base


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    bio = Column(String(500), nullable=True)
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(500), nullable=True)
    publication_date = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship("Author", back_populates="book")
