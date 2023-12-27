from __future__ import annotations

from sqlalchemy.orm import Session

from app import schemas, models


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_all_books(
        db: Session,
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 100
):
    queryset = db.query(models.Book)

    if author_id:
        queryset = queryset.filter(models.Book.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate):

    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(
        models.Author.id == author_id
    ).first()


def get_all_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author
