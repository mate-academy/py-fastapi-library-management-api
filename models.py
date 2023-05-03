from sqlalchemy import Column, Integer, String, func, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(127), unique=True, nullable=False)
    bio = Column(String(511), nullable=True)


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(1023), nullable=True)
    publication_date = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship(DBAuthor)
