from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    Boolean
)
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(63), nullable=False)
    bio = Column(String(511), nullable=False)
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(63), nullable=False)
    summary = Column(String(511), nullable=False)
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship(Author, back_populates="books")
