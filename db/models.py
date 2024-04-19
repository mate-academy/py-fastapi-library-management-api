from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from db.database import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60), unique=True)
    bio = Column(String(550))

    books = relationship("DBBook")


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(60))
    summary = Column(String(500))
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("author.id"))

    authors = relationship(DBAuthor)
