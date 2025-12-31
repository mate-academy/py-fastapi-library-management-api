from sqlalchemy import select, func
from sqlalchemy.orm import Session
import models
import schemas


def get_author_list(
        db: Session,
        skip: int = 0,
        limit: int = 100,
):
    queryset = select(models.DBAuthor)
    queryset = queryset.offset(skip).limit(limit)
    return db.execute(queryset).scalars().all()


def get_author(db: Session, author_id: int):
    stmt = select(models.DBAuthor).where(models.DBAuthor.id == author_id)
    return db.execute(stmt).scalar_one_or_none()


def get_author_by_name(db: Session, name: str):
    name_filter = select(models.DBAuthor).where(
        func.lower(models.DBAuthor.name) == name.strip().lower()
    )
    return db.execute(name_filter).scalar_one_or_none()


def post_author(db: Session, author: schemas.AuthorCreate):
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
        skip: int = 0,
        limit: int = 100,
):
    queryset = select(models.DBBook)

    if author_id is not None:
        queryset = queryset.where(
            models.DBBook.author_id == author_id
        )

    queryset = queryset.offset(skip).limit(limit)

    return db.execute(queryset).scalars().all()


def get_book(db: Session, book_id: int):
    stmt = select(models.DBBook).where(models.DBBook.id == book_id)
    return db.execute(stmt).scalar_one_or_none()


def post_book(
        db: Session,
        book: schemas.BookCreate,
):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
