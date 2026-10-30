from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class DBAuthor(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    bio = Column(String(500), nullable=False)
    books = relationship("DBBook")

class DBBook(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(255), nullable=False)
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"))