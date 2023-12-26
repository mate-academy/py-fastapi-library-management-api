from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    bio = Column(String(1000), nullable=True)

    books = relationship(
        "Book",
        back_populates="author",
        cascade="all, delete",
        passive_deletes=True
    )


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(1000), nullable=True)
    publication_date = Column(Date, nullable=False)
    author_id = Column(
        Integer,
        ForeignKey("authors.id", ondelete="CASCADE"),
        nullable=True
    )

    author = relationship("Author", back_populates="books")
