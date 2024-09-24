from sqlalchemy import Column, Integer, String, ForeignKey, DATE
from sqlalchemy.orm import relationship

from db.engine import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    bio = Column(String(255), nullable=False)

    books = relationship("DBBook")


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(255), nullable=False)
    publication_date = Column(DATE, nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship(DBAuthor)
