from sqlalchemy.orm import Session, joinedload

import schemas
import models


def get_author_list(
        db: Session,
        author_id: int,
        author_name: str,
        limit: int
):
    queryset = db.query(models.DBAuthor)

    if author_id:
        queryset = queryset.filter(models.DBAuthor.id == author_id)

    if author_name:
        queryset = queryset.filter(
            models.DBAuthor.name.ilike(f"%{author_name}%")
        )

    if limit:
        queryset = queryset.limit(limit)
    return queryset.all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(
        models.DBAuthor.id == author_id
    ).first()


def get_author_by_name(db: Session, name: str) -> models.DBAuthor:
    return db.query(models.DBAuthor).filter(
        models.DBAuthor.name == name
    ).first()


def create_author(
        db: Session,
        author: schemas.AuthorCreate
) -> models.DBAuthor:
    db_author = models.DBAuthor(**author.dict())

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_book_list(
        db: Session,
        author_id: int,
        author_name: str,
        book_title: str,
        limit: int
) -> list[models.DBBook]:
    queryset = db.query(
        models.DBBook
    ).options(joinedload(models.DBBook.author))

    if author_id:
        queryset = queryset.filter(models.DBBook.author_id == author_id)

    if author_name:
        queryset = queryset.filter(
            models.DBAuthor.name.ilike(f"%{author_name}%")
        )

    if book_title:
        queryset = queryset.filter(
            models.DBBook.title.ilike(f"%{book_title}%")
        )

    if limit:
        queryset = queryset.limit(limit)

    return queryset.all()


def get_book_by_title(
        db: Session,
        book_title: str,
) -> models.DBBook:
    return db.query(models.DBBook).filter(
        models.DBBook.title == book_title
    ).first()


def create_book(db: Session, book: schemas.BookCreate) -> models.DBBook:
    db_book = models.DBBook(**book.dict())

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
