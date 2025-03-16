from sqlalchemy import Integer, Column, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from db.engine import Base


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, index=True, primary_key=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(511), nullable=False)
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship("DBAuthor", back_populates="books")


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, index=True, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    bio = Column(String(511), nullable=False)
    books = relationship(DBBook, back_populates="author")
