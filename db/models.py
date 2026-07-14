from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date

from db.database import Base


class DBBook(Base):
    __tablename__ = "Book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    summary = Column(String(512), nullable=False)
    publication_date = Column(String(100))
    author_id = Column(Integer, ForeignKey("Author.id"))


class DBAuthor(Base):
    __tablename__ = "Author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False, unique=True)
    bio = Column(String(512), nullable=False)
    books = relationship(DBBook)





