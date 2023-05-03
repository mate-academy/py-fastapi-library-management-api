from datetime import datetime

from sqlalchemy.orm import relationship

from db.engine import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    bio = Column(String(511), nullable=True)


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(511), nullable=True)
    publication_date = Column(DateTime, default=datetime.utcnow, nullable=True)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship(DBAuthor)
