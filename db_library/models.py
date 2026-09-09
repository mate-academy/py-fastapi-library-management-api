from datetime import date
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from db_library.database import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    bio = Column(String)

    books = relationship("DBBook", back_populates="author")


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    summary = Column(String)
    publication_date = Column(Date, default=date.today)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship(DBAuthor)
