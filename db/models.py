from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from db.engine import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(63), unique=True, nullable=False)
    bio = Column(String(511), nullable=False)

    books = relationship("DBBook", back_populates="authors")


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(511), nullable=False)
    publication_date = Column(Date, nullable=False)
    authors_id = Column(Integer, ForeignKey("author.id"), nullable=False)

    authors = relationship("DBAuthor", back_populates="books")
