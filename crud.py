from sqlalchemy.orm import Session, Query

import models
import schemas


def str_to_int(author_ids: str) -> list[int]:
    return list(map(int, author_ids.split(",")))


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_author(
    db: Session, skip: int = 0, limit: int | None = None
) -> list[models.Author]:
    queryset = db.query(models.Author)
    if limit:
        queryset = queryset.limit(limit)
    if skip:
        queryset = queryset.offset(skip * limit)
    return queryset.all()


def get_author(db: Session, author_id: int) -> models.Author:
    return (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )


def get_author_by_name(db: Session, name: str) -> models.Author:
    return db.query(models.Author).filter(models.Author.name == name).first()


def update_author(
    db: Session, db_author: models.Author, author: schemas.AuthorUpdate
) -> models.Author:
    for key, value in author.dict(exclude_unset=True).items():
        setattr(db_author, key, value)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int) -> int:
    num_deleted_authors = (
        db.query(models.Author).filter(models.Author.id == author_id).delete()
    )
    db.commit()
    return num_deleted_authors


def get_books_list(
    db: Session,
    author_ids: str | None = None,
    skip: int = 0,
    limit: int | None = None,
) -> list[models.Book]:
    queryset = db.query(models.Book)

    if author_ids:
        author_ids = str_to_int(author_ids)
        queryset = queryset.filter(models.Book.author.id.in_(author_ids))

    if limit:
        queryset = queryset.limit(limit)
    if skip:
        queryset = queryset.offset(skip * limit)
    return queryset.all()


def get_book_by_title(db: Session, title: str) -> models.Book:
    return db.query(models.Book).filter(models.Book.title == title).first()


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


def get_book(db: Session, book_id: int) -> models.Book:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def update_book(
    db: Session, db_book: models.Book, book: schemas.BookUpdate
) -> models.Book:
    for key, value in book.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> int:
    num_deleted_books = (
        db.query(models.Author).filter(models.Author.id == book_id).delete()
    )
    db.commit()
    return num_deleted_books
