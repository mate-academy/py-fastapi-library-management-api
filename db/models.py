from sqlalchemy import Column, String, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.engine import Base


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    summary = Column(String(255), nullable=True)
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship("DBAuthor")


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    bio = Column(String(255), nullable=True)
    books = relationship(DBBook, back_populates="author")
