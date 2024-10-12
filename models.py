from sqlalchemy import Column, Integer, String, Date, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class DbAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    bio = Column(String(511), nullable=False)

    books = relationship("Book", back_populates="author")


class DbBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(511), nullable=False)
    publication_date = Column(Date(), nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship("DbAuthor", back_populates="books")

    __table_args__ = (
        CheckConstraint('publication_date <= CURRENT_DATE', name='publication_date'),
    )
