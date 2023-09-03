from sqlalchemy.orm import Session
from schemas import AuthorCreate, Book, BookCreate

import models


def get_authors_list(db: Session):
    return db.query(models.Author).all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(models.Author).filter(
        models.Author.id == author_id
    ).first()


def create_author(db: Session, author: AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_book_list(db: Session, author_id: int):

    queryset = db.query(models.Book)

    if author_id:
        queryset = queryset.filter(models.Book.author_id == author_id)

    return queryset.all()


def create_book(db: Session, book: BookCreate):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
