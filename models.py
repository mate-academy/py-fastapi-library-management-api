from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    name = Column(
        String(100),
        unique=True,
        nullable=False
    )
    bio = Column(
        String(255),
        nullable=False
    )


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String(255), nullable=False)
    publication_date = Column(
        Date,
        nullable=False,
        default=func.current_date()
    )
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship(DBAuthor)
