from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
import models


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 100,
) -> list[models.Author]:
    return db.scalars(
        select(models.Author)
        .offset(skip)
        .limit(limit)
    ).all()


def get_author_by_id(
        db: Session, author_id: int
) -> models.Author | None:
    return db.scalar(
        select(models.Author).where(models.Author.id == author_id)
    )


def create_author(
        db: Session,
        author: schemas.AuthorCreate
) -> models.Author:
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def update_author(
        db: Session,
        author_id: int,
        author: schemas.AuthorUpdate,
) -> models.Author | None:
    db_author = get_author_by_id(db, author_id)

    if db_author is None:
        return None

    for key, value in author.model_dump(exclude_unset=True).items():
        setattr(db_author, key, value)

    db.commit()
    db.refresh(db_author)

    return db_author


def delete_author(
        db: Session,
        author_id: int,
) -> bool:
    db_author = get_author_by_id(db, author_id)

    if db_author is None:
        return False

    db.delete(db_author)
    db.commit()

    return True


def get_all_books(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        author_id: int | None = None,
) -> list[models.Book]:
    query = select(models.Book)

    if author_id is not None:
        query = query.where(models.Book.author_id == author_id)

    return db.scalars(
        query
        .offset(skip)
        .limit(limit)
    ).all()


def get_book_by_id(db: Session, book_id: int) -> models.Book | None:
    result = db.execute(
        select(models.Book).where(models.Book.id == book_id)
    )
    return db.scalar(
        select(models.Book).where(models.Book.id == book_id)
    )


def create_book(
        db: Session,
        book: schemas.BookCreate,
) -> models.Book:
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


def update_book(
        db: Session,
        book_id: int,
        book: schemas.BookUpdate,
) -> models.Book | None:
    db_book = get_book_by_id(db, book_id)

    if db_book is None:
        return None

    for key, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)

    return db_book


def delete_book(
        db: Session,
        book_id: int,
) -> bool:
    db_book = get_book_by_id(db, book_id)

    if db_book is None:
        return False

    db.delete(db_book)
    db.commit()

    return True
