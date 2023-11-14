from sqlalchemy.orm import Session

from db import models, schemas
from db.models import DBAuthor, DBBook


def get_author_by_name(
    db: Session,
    name: str,
) -> DBAuthor | None:
    return db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()


def get_all_authors(db: Session, page: int = 0, page_size: int = 20) -> list[DBAuthor]:
    return db.query(models.DBAuthor).offset(page).limit(page_size).all()


def get_detailed_author(db: Session, author_id: int = None) -> DBAuthor | None:
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate) -> DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_books(
    db: Session, author_id: int = None, page: int = 0, page_size: int = 20
) -> list[DBBook]:
    queryset = db.query(models.DBBook)
    if author_id:
        queryset = (
            db.query(models.DBBook)
            .filter(models.DBBook.author_id == author_id)
        )
    queryset = queryset.offset(page).limit(page_size).all()
    return queryset


def create_book(db: Session, book_data: schemas.BookCreate) -> DBBook:
    db_book = models.DBBook(
        **book_data.model_dump(),
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_detailed_book(db: Session, book_id: int = None) -> DBBook | None:
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()


def delete_book(db: Session, book_id: int) -> DBBook | None:
    db_book = get_detailed_book(db=db, book_id=book_id)
    if db_book is not None:
        db.delete(db_book)
        db.commit()

    return db_book
