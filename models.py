from sqlalchemy import (
    Column, Integer, String, Date, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship

from database import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    bio = Column(String(511))
    books = relationship("DBBook", back_populates="author")

    def __repr__(self):
        return f"<DBAuthor(id={self.id}, name={self.name})>"


class DBBook(Base):
    __tablename__ = "book"
    __table_args__ = (
        UniqueConstraint("id", "author_id"),
    )

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    summary = Column(String(511))
    publication_date = Column(Date)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship("DBAuthor", back_populates="books")

    def __repr__(self):
        return f"<DBBook(id={self.id}, title={self.title})>"
