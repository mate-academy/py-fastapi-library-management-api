from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
import models


def get_all_authors(db: Session) -> list[models.DBAuthor]:

    return paginate(db, select(models.DBAuthor)).all()


def get_author_by_name(db: Session, name: str) -> models.DBAuthor | None:
    return db.scalar(
        select(models.DBAuthor).where(models.DBAuthor.name == name)
    )


def get_author_by_id(db: Session, author_id: int) -> models.DBAuthor | None:
    return db.scalar(
        select(models.DBAuthor).where(models.DBAuthor.id == author_id)
    )


def create_author(
    db: Session, author: schemas.AuthorCreate
) -> models.DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_book_list(
    db: Session,
    author_id: int | None = None,
) -> list[models.DBBook]:
    queryset = select(models.DBBook)
    if author_id:
        queryset = queryset.join(models.DBAuthor).where(
            models.DBAuthor.id == author_id
        )

    return paginate(db, queryset)


def get_book_by_id(db: Session, book_id: int) -> models.DBBook | None:
    return db.scalar(select(models.DBBook).where(models.DBBook.id == book_id))


def create_book(db: Session, book: schemas.BookCreate) -> models.DBBook:
    db_book = models.DBBook(
        author_id=book.author_id,
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
