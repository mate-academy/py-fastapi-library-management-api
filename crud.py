from sqlalchemy.orm import Session

import models
import schemas


def get_author(db: Session, id: int):
    return db.query(models.Author).get(id)


def get_all_authors(
    db: Session, skip: int | None, limit: int | None
):
    query = db.query(models.Author)
    if skip:
        query = query.offset(skip)
    if limit:
        query = query.limit(limit)

    return query.all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_books(
    db: Session,
    author_id: int | None,
    skip: int | None,
    limit: int | None,
):
    query = db.query(models.Book)
    if author_id:
        query = query.filter(models.Book.author_id == author_id)
    if skip:
        query = query.offset(skip)
    if limit:
        query = query.limit(limit)

    return query.all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
