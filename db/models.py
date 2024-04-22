from datetime import date

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class DbAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    bio = Column(String(511), nullable=False)
    books = relationship("DbBook", back_populates="author")


class DbBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(511), nullable=False)
    publication_date = Column(Date, default=date.today(), nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    author = relationship("DbAuthor", back_populates="books")
