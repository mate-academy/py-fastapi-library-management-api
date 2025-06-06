

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship 
from database import Base



class DbBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    summary = Column(String(500), nullable=False)
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship("DbAuthor", back_populates="books")


class DbAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, unique=True)
    bio = Column(String(500), nullable=False)

    books = relationship("DbBook", back_populates="author")
