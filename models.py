from sqlalchemy.orm import relationship

from database import Base

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
)


class DBBook(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(1023), nullable=True)
    publication_date = Column(Date, nullable=True)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    author = relationship("DBAuthor", back_populates="books")


class DBAuthor(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    bio = Column(String(511), nullable=True)

    books = relationship("DBBook", back_populates="author")
