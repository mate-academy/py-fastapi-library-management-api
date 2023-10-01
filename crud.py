from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(
    db: Session,
    skip: int = 0,
    limit: int = 4
):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def create_authors(db: Session, author: schemas.AuthorCreate):
    db_authors = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_authors)
    db.commit()
    db.refresh(db_authors)
    return db_authors


def get_author(db: Session, author_id: int):
    return (db.query(models.DBAuthor).
            filter(models.DBAuthor.id == author_id).first())


def get_all_books(
    db: Session,
    author_id: int | None = None,
    skip: int = 0,
    limit: int = 4
):
    queryset = db.query(models.DbBook)

    if author_id is not None:
        queryset = queryset.filter(
            models.DbBook.author_id == author_id
        )
    return queryset.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DbBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
