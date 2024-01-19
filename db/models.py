from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    bio = Column(String(500))


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(500))
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship(DBAuthor)
