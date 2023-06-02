from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(type_=Integer, primary_key=True, index=True)
    name = Column(type_=String(255), nullable=False, unique=True)
    bio = Column(type_=String(511), nullable=False)
    books = relationship("DBBook", backref="author")


class DBBook(Base):
    __tablename__ = "book"

    id = Column(type_=Integer, primary_key=True, index=True)
    title = Column(type_=String(255), nullable=False)
    summary = Column(type_=String(511), nullable=False)
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"))
