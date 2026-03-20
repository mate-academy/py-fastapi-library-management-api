from typing import Annotated
from datetime import date

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped

from db.database import Base


str_256 = Annotated[str, mapped_column(String(256))]
str_512 = Annotated[str, mapped_column(String(512))]
intpk = Annotated[int, mapped_column(primary_key=True)]


class AuthorORM(Base):
    __tablename__ = "Author"
    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(256), unique=True)
    bio: Mapped [str_512]

    books: Mapped[list["BookORM"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )


class BookORM(Base):
    __tablename__ = "Book"
    id: Mapped[intpk]
    title: Mapped[str_256]
    summary: Mapped[str_512]
    publication_date: Mapped[date]

    author_id: Mapped[int] = mapped_column(ForeignKey("Author.id", ondelete="CASCADE"))
    author: Mapped["AuthorORM"] = relationship(back_populates="books")
