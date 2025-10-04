from enum import StrEnum, auto
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship
from library_book.database import Base


class PackagingType(StrEnum):
    IN_PACKAGE = auto()
    WEIGHT = auto()


class LBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    bio = Column(String(255), nullable=False)
    books = relationship("LBBook", back_populates="author")


class LBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, unique=True)
    summary = Column(String(255), nullable=False)
    publication_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"))
    packaging_type = Column(Enum(PackagingType), nullable=False)

    author = relationship(LBAuthor, back_populates="books")
