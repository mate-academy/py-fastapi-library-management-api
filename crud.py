from sqlalchemy.orm import Session

import models
import schemas


def get_author(db: Session, author_id: int):
    return (
        db.query(models.DBAuthor)
        .filter(models.DBAuthor.id == author_id)
        .first()
    )


def get_all_authors(db: Session, name: str | None = None):
    queryset = db.query(models.DBAuthor)

    if name is not None:
        queryset = queryset.filter(models.DBAuthor.name == name)

    return queryset.all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_book(db: Session, book_id: int):
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()


def get_all_books(
    db: Session, title: str | None = None, author_id: int | None = None
):
    queryset = db.query(models.DBBook)

    if title is not None:
        queryset = queryset.filter(models.DBBook.title == title)

    if author_id is not None:
        queryset = queryset.filter(models.DBBook.author_id == author_id)

    return queryset.all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
