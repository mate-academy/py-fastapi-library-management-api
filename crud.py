from datetime import date

from sqlalchemy.orm import Session

import models, schemas


def get_all_authors(db_session: Session):
    authors = db_session.query(models.Author).all()
    return authors


def get_author_by_name(db_session: Session, name: str):
    return db_session.query(models.Author).filter(models.Author.name == name).first()


def get_author_by_id(db_session: Session, author_id: int):
    return db_session.query(models.Author).filter(models.Author.id == author_id).first()


def create_author(db_session: Session, author: schemas.AuthorCreate):
    db_new_author = models.Author(name=author.name, bio=author.bio)
    db_session.add(db_new_author)
    db_session.commit()
    db_session.refresh(db_new_author)
    return db_new_author


def get_all_books(db_session: Session, author_id: int | None = None):
    queryset = db_session.query(models.Book)
    if author_id:
        queryset = queryset.filter(models.Book.author_id == author_id)
    return queryset.all()


def create_book(db_session: Session, book: schemas.BookCreate):
    if isinstance(book.publication_date, str):
        book.publication_date = date.fromisoformat(book.publication_date)

    db_new_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db_session.add(db_new_book)
    db_session.commit()
    db_session.refresh(db_new_book)
    return db_new_book
