from sqlalchemy import String, Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from db.database import Base


class DBAuthor(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    bio = Column(String(500))
    books = relationship("DBBook")


class DBBook(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    summary = Column(String(500))
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("authors.id"))
