from sqlalchemy.orm import Session

import schemas
import models


def get_all_authors(db: Session):
    return db.query(models.Author).all()


def get_author_by_id(db: Session, author_id: int) -> models.Author | None:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_books(
        db: Session,
        author_id: str | None = None,
        skip: int | None = None,
        limit: int | None = None
) -> list[models.Book]:
    queryset = db.query(models.Book)

    if author_id:
        queryset = (
            queryset.join(models.Book.author)
            .filter(models.Author.id == author_id)
        )

    if limit:
        queryset = queryset.limit(limit)

    if skip:
        queryset = queryset.offset(skip)

    return queryset.all()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
