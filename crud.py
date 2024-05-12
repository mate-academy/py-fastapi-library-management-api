from sqlalchemy.orm import Session
import models
import schemas


def create_author(
        db: Session,
        author: schemas.AuthorCreate
) -> models.DBAuthor:
    db_author = models.DBAuthor(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author(db: Session, author_id: int) -> models.DBAuthor | None:
    return db.query(models.DBAuthor).filter(
        models.DBAuthor.id == author_id
    ).first()


def get_authors(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> list[models.DBAuthor]:
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def create_book(
        db: Session,
        book: schemas.BookCreate,
        author_id: int,
) -> models.DBBook:
    db_book = models.DBBook(**book.model_dump(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session, book_id: int) -> models.DBBook | None:
    return db.query(models.DBBook).filter(
        models.DBBook.id == book_id
    ).first()


def get_books(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> list[models.DBBook]:
    return db.query(models.DBBook).offset(skip).limit(limit).all()
