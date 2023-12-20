from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class DBAuthor(Base):
    """Database model for authors."""
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    bio = Column(String(511), nullable=False)

    books = relationship("DBBook", back_populates="author")


class DBBook(Base):
    """Database model for books."""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(511), nullable=False)
    publication_date = Column(Date, nullable=False)

    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("DBAuthor", back_populates="books")
