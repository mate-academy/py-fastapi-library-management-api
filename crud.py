from sqlalchemy.orm import Session

import models
import schemas


def get_authors_list(
        db: Session,
        offset: int = None,
        limit: int = None,
) -> [models.Author]:
    query = db.query(models.Author)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()


def get_single_author(
        db: Session,
        author_id: int
) -> models.Author | None:
    return db.query(models.Author).filter(
        models.Author.id == author_id
    ).first()


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


def get_books_list(
    db: Session,
    offset: int = None,
    limit: int = None,
    author_id: int = None,
) -> [models.Book]:
    query = db.query(models.Book)
    if author_id:
        query = query.filter(models.Book.author_id == author_id)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()


def get_single_book(
        db: Session,
        book_id: int
) -> models.Book | None:
    return db.query(models.Book).filter(
        models.Book.id == book_id
    ).first()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(
        title=book.title,
        author_id=book.author_id,
        summary=book.summary,
        publication_date=book.publication_date
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
