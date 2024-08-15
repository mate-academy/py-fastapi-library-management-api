from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session, limit: int = 0, offset: int = 0) -> models.DBAuthor:
    return db.query(models.DBAuthor).limit(limit).offset(offset)


def get_author_type_by_name(db: Session, name: str) -> models.DBAuthor:
    return (
        db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()
    )


def create_author(db: Session, author: schemas.AuthorCreate) -> models.DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_books_list(db: Session, author_id: int | None = None, limit: int = 0, offset: int = 0) -> models.DBBook:
    queryset = db.query(models.DBBook)

    if author_id is not None:
        queryset = queryset.filter(models.DBBook.author.has(id=author_id))

    return queryset.limit(limit).offset(offset)


def get_book(db: Session, book_id: int) -> models.DBBook:
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()


def get_author(db: Session, author_id: int) -> models.DBAuthor:
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def create_book(db: Session, book: schemas.BookCreate) -> models.DBBook:
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
