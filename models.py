from sqlalchemy import Column, Integer, String, DATE, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(333))
    publication_date = Column(DATE)
    author_id = Column(Integer, ForeignKey("author.id"))


class DBAuthor(Base):
    __tablename__ = "author"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    bio = Column(String(555))
    books = relationship(DBBook)
