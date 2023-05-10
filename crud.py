from sqlalchemy.orm import Session

from db import models
import schemas


def get_all_authors(db: Session):
    return db.query(models.DBAuthor).all()


def get_author(db: Session, author_id: int):
    return (
        db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()
    )


def get_all_authors_by_name(db: Session, name: str):
    return (
        db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()
    )


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_books_list(db: Session, author_id: int = None):
    queryset = db.query(models.DBBook)

    if author_id is not None:
        queryset = queryset.filter(models.DBBook.author.has(id=author_id))

    return queryset.all()


def get_all_books_by_title(db: Session, title: str):
    return (
        db.query(models.DBBook).filter(models.DBBook.title == title).first()
    )


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
