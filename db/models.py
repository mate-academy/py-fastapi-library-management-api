from datetime import date
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from db.database import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(55), nullable=False, unique=True)
    bio = Column(String(512), nullable=False)
    books = relationship("DBBook", back_populates="author")


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(55), nullable=False)
    summary = Column(String(512), nullable=False)
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    author = relationship("DBAuthor", back_populates="books")
