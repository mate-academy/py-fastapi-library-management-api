from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class DBBook(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    summary = Column(String(255))
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("authors.id"))


class DBAuthor(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    bio = Column(String(255))
    books = relationship(DBBook)
