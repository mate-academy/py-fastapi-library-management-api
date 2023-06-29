from sqlalchemy.orm import Session

import models
from schemas import AuthorBaseCreate, BookBaseCreate


def get_all_authors(db: Session):
    return db.query(models.Author).all()


def get_author_by_name(db: Session, name: str):
    return db.query(models.Author).filter(models.Author.name == name).first()


def get_author_by_id(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def create_author(db: Session, author: AuthorBaseCreate):
    db_authors = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_authors)
    db.commit()
    db.refresh(db_authors)
    return db_authors


def create_book_for_author(db: Session, book: BookBaseCreate, author_id: int):
    db_book = models.Book(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_all_books(db: Session, author_id: int | None = None):
    queryset = db.query(models.Book)

    if author_id:
        queryset = queryset.filter(models.Book.author_id == author_id)
    return queryset.all()
