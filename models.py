from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    bio = Column(String(511))
    books = relationship("DBBook", back_populates="author")


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    summary = Column(String(511))
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship(DBAuthor, back_populates="books")
