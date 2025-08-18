from datetime import datetime

from sqlalchemy.orm.session import Session

from database.models import AuthorModel, BookModel


def create_new_author(db: Session, name: str, bio: str) -> AuthorModel:
    author = AuthorModel(name=name, bio=bio)

    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def get_authors_paginated(db: Session, skip: int, limit: int) -> list[AuthorModel]:
    authors = db.query(AuthorModel).offset(skip).limit(limit).all()
    return authors


def get_single_author(db: Session, author_id: int) -> AuthorModel:
    author = db.query(AuthorModel).filter_by(id=author_id).first()
    return author


def create_new_book_for_specific_author(
    db: Session,
    author_id: int,
    title: str,
    summary: str,
    publication_date: datetime.date,
) -> BookModel:
    book = BookModel(
        author_id=author_id,
        title=title,
        summary=summary,
        publication_date=publication_date,
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


def get_books_paginated(db: Session, skip: int, limit: int) -> list[BookModel]:
    books = db.query(BookModel).offset(skip).limit(limit).all()
    return books


def get_books_by_author_id(db: Session, author_id: int) -> list[BookModel]:
    books = db.query(BookModel).filter_by(author_id=author_id).all()
    return books
