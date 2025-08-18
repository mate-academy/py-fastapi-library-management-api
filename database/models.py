from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Date

from .database import Base


class AuthorModel(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    bio: Mapped[str] = mapped_column(String)

    books: Mapped[list["BookModel"]] = relationship(
        "BookModel", back_populates="author"
    )


class BookModel(Base):
    __tablename__ = "books"

    id = mapped_column(Integer, primary_key=True, nullable=False)
    title = mapped_column(String, nullable=False)
    summary = mapped_column(String)
    publication_date = mapped_column(Date)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id", ondelete="CASCADE"), nullable=False
    )

    author: Mapped["AuthorModel"] = relationship("AuthorModel", back_populates="books")
