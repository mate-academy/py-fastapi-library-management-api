from datetime import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class DBAuthor(Base):
    __tablename__ = "author"

    id: Mapped["int"] = mapped_column(primary_key=True, index=True)
    name: Mapped["str"] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )
    bio: Mapped["str"] = mapped_column(String(255))
    books: Mapped[list["DBBook"] | None] = relationship(
        back_populates="author"
    )


class DBBook(Base):
    __tablename__ = "book"

    id: Mapped["int"] = mapped_column(primary_key=True, index=True)
    title: Mapped["str"] = mapped_column(String(255), nullable=False)
    summary: Mapped["str"] = mapped_column(String(255))
    publication_date: Mapped[datetime] = mapped_column()
    author_id: Mapped[int | None] = mapped_column(
        ForeignKey("author.id"), nullable=True
    )
    author: Mapped[DBAuthor | None] = relationship(back_populates="books")
