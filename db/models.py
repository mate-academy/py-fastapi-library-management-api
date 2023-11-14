from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from db.engine import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=False)
    name = Column(String(64), nullable=False, unique=True)
    bio = Column(String(255))
    books = relationship("Book", back_populates="author")


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=False)
    title = Column(String(64), nullable=False)
    summary = Column(String(511))
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship("DBAuthor", back_populates="books")
