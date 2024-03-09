from sqlalchemy import (
    Integer,
    String,
    Date,
    Column,
    ForeignKey,
    func
)
from sqlalchemy.orm import relationship

from database import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    bio = Column(String(1000), nullable=True)
    # define one-to-many relationship with DBBook
    books = relationship("DBBook", back_populates="author")


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False, unique=True)
    summary = Column(String(1000), nullable=False)
    publication_date = Column(Date, default=func.now())

    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship("DBAuthor", back_populates="books")
