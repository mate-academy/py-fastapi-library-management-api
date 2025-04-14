from sqlalchemy.orm import Session, selectinload

import models
import schemas


def get_book_list(db: Session) -> list[models.DBBook]:
    return db.query(models.DBBook).all()


def get_book(db: Session, author_id: int) -> models.DBBook:
    return (
        db.query(models.DBBook)
        .options(selectinload(models.DBBook.author_id))
        .filter(models.DBBook.author_id == author_id)
        .first()
    )


def get_books_by_author(db: Session, author_id: int) -> list[models.DBBook]:
    return db.query(models.DBBook).filter(models.DBBook.author_id == author_id).all()


def create_book(
    db: Session,
    book: schemas.BookCreate,
    author_id: int,
) -> models.DBBook:
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_all_author_list(db: Session) -> list[models.DBAuthor]:
    return db.query(models.DBAuthor).all()


def get_author(db: Session, books: int) -> models.DBAuthor:
    return (
        db.query(models.DBAuthor)
        .options(selectinload(models.DBAuthor.books))
        .filter(models.DBAuthor.books.id == books.id)
        .first()
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
