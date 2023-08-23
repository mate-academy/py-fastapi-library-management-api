from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from data_base.database import Base


class DBAuthor(Base):
    __tablename__ = "authors"

    id = Column(Integer)
    name = Column(String(63), nullable=False, unique=True)
    bio = Column(String(511), nullable=False, unique=True)

    books = relationship("DBBook", back_populates="author")


class DBBook(Base):
    __tablename__ = "books"

    id = Column(Integer)
    title = Column(String(63), nullable=False, unique=True)
    summary = Column(String(63), nullable=False)
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("books.id"))

    author = relationship("DBAuthor", back_populates="books")


