from sqlalchemy.orm import relationship
from data_base.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey
)


class DBAuthor(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(63), nullable=False, unique=True)
    bio = Column(String(511), nullable=False, unique=True)

    books = relationship("DBBook", back_populates="author")


class DBBook(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(63), nullable=False, unique=True)
    summary = Column(String(63), nullable=False)
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship(DBAuthor, back_populates="books")
