from sqlalchemy import Integer, Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from db.engine import Base


class DBAuthorType(Base):
    __tablename__ = "author_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    bio = Column(String(511), nullable=False)
    books = relationship("Book", back_populates="author_type")


class DBBookType(Base):
    __tablename__ = "book_type"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, unique=True)
    summary = Column(String(511), nullable=False)
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("author_type.id"), nullable=False)

    author_type = relationship(DBAuthorType)