from sqlalchemy.orm import Session

from db import models
import schemas


def get_all_authors(db: Session) -> list[models.DBAuthor]:
    return db.query(models.DBAuthor).all()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.DBAuthor:
    db_author = models.DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author_by_id(db: Session, author_id: int) -> models.DBAuthor:
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def get_author_by_name(db: Session, name: str) -> models.DBAuthor:
    return db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()


def get_book_list(db: Session) -> list[models.DBBook]:
    queryset = db.query(models.DBBook).all()

    return queryset


def get_book(db: Session, book_id: int) -> models.DBBook:
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate) -> models.DBBook:
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        published_date=book.published_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def filter_books_by_author(db: Session, author_id: int) -> list[models.DBBook]:
    return db.query(models.DBBook).filter(models.DBBook.author_id == author_id).all()
