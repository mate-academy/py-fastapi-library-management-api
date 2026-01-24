from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"


class Author(Base):
    name: Mapped[str] = mapped_column(unique=True)
    bio: Mapped[str]
    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Book(Base):
    title: Mapped[str]
    summary: Mapped[str]
    publication_date: Mapped[date]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["Author"] = relationship(back_populates="books")
