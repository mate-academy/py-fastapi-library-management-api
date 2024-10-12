from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(
        db: Session,
        skip: int | None,
        limit: int | None = None,
) -> list[models.Author]:
    query = db.query(models.Author)

    if limit:
        query = query.limit(limit)

    if skip:
        query = query.offset(skip)

    return query.all()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author_detail(db: Session, id: int) -> models.Author:
    return db.query(models.Author).filter(models.Author.id == id).first()


def get_all_books(
        db: Session,
        skip: int | None,
        limit: int | None,
        author_id: int | None = None,
) -> list[models.Book]:
    query = db.query(models.Book)

    if author_id:
        query = query.filter(models.Book.author_id == author_id)

    if limit:
        query = query.limit(limit)

    if skip:
        query = query.offset(skip)

    return query.all()


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
