from app import models, schemas
from sqlalchemy.orm import Session


def get_author_by_id(db: Session, author_id: int):
    return (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )


def get_author_by_name(db: Session, author_name: str):
    return (
        db.query(models.Author)
        .filter(models.Author.name == author_name)
        .first()
    )


def get_author_list(db: Session, skip: int = 0, limit: int = 5):
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_book_list(db: Session, skip: int = 0, limit: int = 5):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book_list_by_author_id(db: Session, author_id: int):
    return (
        db.query(models.Book).filter(models.Book.author_id == author_id).all()
    )


def create_book(db: Session, book: schemas.BookCreate, author_id: int):
    db_book = models.Book(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
