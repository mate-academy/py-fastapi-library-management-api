from sqlalchemy.orm import Session

import models
from schemas import AuthorCreate, BookCreate


def get_all_authors(db: Session):
    authors = db.query(models.Authors).all()
    return db.query(models.Authors).all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(models.Authors).filter(models.Authors.id == author_id).first()


def create_author(db: Session, author_create: AuthorCreate):
    db_author = models.Authors(
        name=author_create.name,
        bio=author_create.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_books(db: Session,
                  author: int | None = None,
                  ):
    queryset = db.query(models.Book)

    if author is not None:
        queryset = queryset.filter(models.Book.author.has(id=author))

    return queryset.all()


def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(db: Session, book_create: BookCreate):
    db_book = models.Book(
        title=book_create.title,
        summary=book_create.summary,
        publication_date=book_create.publication_date,
        author_id=book_create.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
