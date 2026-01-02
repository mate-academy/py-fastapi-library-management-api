from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class DBAuthor(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)

    name = Column(String,nullable=False, unique=True)
    bio = Column(String, nullable=False)
    books = relationship("DBBook", backref="author")

class DBBook(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False,)