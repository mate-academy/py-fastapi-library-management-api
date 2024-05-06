from sqlalchemy.orm import Session

from library import models, schemas


def get_authors(
    db: Session, skip: int = 0, limit: int = 2
) -> list[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int) -> models.Author | None:
    return (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_books(
    db: Session, skip: int = 0, limit: int = 2, author_id: int | None = None
) -> list[models.Book]:
    queryset = db.query(models.Book)

    if author_id is not None:
        queryset = queryset.filter(models.Book.author_id == author_id)

    queryset = queryset.offset(skip).limit(limit)

    return queryset.all()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
