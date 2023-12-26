from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session, limit: int, offset: int):
    return db.query(models.DBAuthor).limit(limit).offset(offset)


def get_all_books(db: Session, limit: int, offset: int):
    return db.query(models.DBBook).limit(limit).offset(offset)


def get_author_by_name(db: Session, name: str):
    return (
        db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()
    )


def get_book_by_title(db: Session, title: str):
    return (
        db.query(models.DBBook).filter(models.DBBook.title == title).first()
    )


def get_author(db: Session, author_id: int):
    return (
        db.query(models.DBAuthor).
        filter(models.DBAuthor.id == author_id).first()
    )


def get_book(db: Session, book_id: int):
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        authors=book.authors
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_book_list(
    db: Session,
    author_id: int | None = None,
):
    queryset = db.query(models.DBBook)

    if author_id:
        queryset = queryset.filter(
            models.DBBook.authors.has(id == author_id)
        )

    return queryset.all()
