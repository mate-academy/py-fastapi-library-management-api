from typing import List, Optional

from sqlalchemy.orm import Session

from db import models
import schemas


def get_all_authors(
    db: Session, skip: int = 0, limit: int = 5
) -> List[models.DBAuthor]:
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author_by_name(db: Session, name: str) -> Optional[models.DBAuthor]:
    return (
        db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()
    )


def get_author(db: Session, author_id: int) -> Optional[models.DBAuthor]:
    return (
        db.query(models.DBAuthor)
        .filter(models.DBAuthor.id == author_id)
        .first()
    )


def create_author(
    db: Session, author: schemas.AuthorCreate
) -> models.DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(
    db: Session, author_id: int, author: schemas.Author
) -> Optional[models.DBAuthor]:
    db_author = (
        db.query(models.DBAuthor)
        .filter(models.DBAuthor.id == author_id)
        .first()
    )
    if not db_author:
        return None
    for field, value in vars(author).items():
        if value is not None:
            setattr(db_author, field, value)
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int) -> Optional[models.DBAuthor]:
    db_author = (
        db.query(models.DBAuthor)
        .filter(models.DBAuthor.id == author_id)
        .first()
    )
    if not db_author:
        return None
    db.delete(db_author)
    db.commit()
    return db_author


def get_book_list(
    db: Session,
    author: Optional[str] = None,
    skip: int = 0,
    limit: int = 5,
) -> List[models.DBBook]:
    queryset = db.query(models.DBBook).offset(skip).limit(limit)

    if author is not None:
        queryset = queryset.filter(models.DBBook.author == author)

    return queryset.all()


def get_book(db: Session, book_id: int) -> Optional[models.DBBook]:
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()


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


def update_book(
    db: Session, book_id: int, book: schemas.BookBase
) -> Optional[models.DBBook]:
    db_book = (
        db.query(models.DBBook).filter(models.DBBook.id == book_id).first()
    )
    if not db_book:
        return None
    for field, value in vars(book).items():
        if value is not None:
            setattr(db_book, field, value)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> Optional[models.DBBook]:
    db_book = (
        db.query(models.DBBook).filter(models.DBBook.id == book_id).first()
    )
    if not db_book:
        return None
    db.delete(db_book)
    db.commit()
    return db_book
