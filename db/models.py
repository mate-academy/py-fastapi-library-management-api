from sqlalchemy import Integer, Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from db.engine import Base


class DBBook(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True, nullable=False)
    summary = Column(String(511), nullable=False)
    publication_date = Column(Date)

    author_id = Column(Integer, ForeignKey("authors.id"))


class DBAuthor(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    bio = Column(String(511), nullable=False)

    books = relationship(DBBook)
