from sqlalchemy.orm import Session
import models
import schemas


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_authors(
        db: Session,
        skip: int = 0,
        limit: int = 50
) -> list[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int) -> models.Author:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def create_author_book(db: Session, book: schemas.BookCreate, author_id: int) -> models.Book:
    db_book = models.Book(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(
        db: Session,
        skip: int = 0,
        limit: int = 50
) -> list[models.Book]:
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book_by_author_id(db: Session, author_id: int) -> models.Book:
    return db.query(models.Book).filter(models.Book.author_id == author_id).first()
