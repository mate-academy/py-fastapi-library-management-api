from sqlalchemy import update
from sqlalchemy.orm import Session

import models
from schemas import AuthorCreate, BookCreate, AuthorUpdate


def create_author(db: Session, author: AuthorCreate) -> models.DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(db: Session, author_id: int, author: AuthorUpdate) -> models.DBAuthor | None:
    author_for_update = get_author(db, author_id)
    data_for_update = {}
    if author_for_update is not None:
        for field, value in author.dict().items():
            if value:
                data_for_update[field] = value
        db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).update(data_for_update)
        db.commit()
        db.refresh(author_for_update)
        return author_for_update


def delete_author(db: Session, author_id: int) -> models.DBAuthor | None:
    author_to_delete = get_author(db, author_id)

    if author_to_delete is not None:
        db.delete(author_to_delete)
        db.commit()
        return author_to_delete


def get_all_authors(db: Session, skip: int = 0, limit: int = 10) -> list[models.DBAuthor]:
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int) -> models.DBAuthor | None:
    return (
        db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()
    )


def get_author_by_name(db: Session, name: str) -> models.DBAuthor | None:
    return (
        db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()
    )


def create_book(db: Session, book: BookCreate) -> models.DBBook:
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_all_books(db: Session, author: str | None = None, skip: int = 0, limit: int = 10) -> list[models.DBAuthor]:
    queryset = db.query(models.DBBook)
    if author is not None:
        queryset = queryset.filter(
            models.DBBook.author == author
        )
    return queryset.offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> models.DBBook | None:
    return (
        db.query(models.DBBook).filter(models.DBBook.id == book_id).first()
    )


def delete_book(db: Session, book_id: int) -> models.DBBook | None:
    book_to_delete = get_book(db, book_id)

    if book_to_delete is not None:
        db.delete(book_to_delete)
        db.commit()
        return book_to_delete


def get_book_by_title(db: Session, title: str) -> models.DBBook | None:
    return (
        db.query(models.DBBook).filter(models.DBBook.title == title).first()
    )
