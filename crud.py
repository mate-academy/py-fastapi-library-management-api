from sqlalchemy.orm import Session

import schemas
from models import DBAuthor, DBBook


def get_authors_list(
        db: Session,
        skip: int | None = None,
        limit: int | None = None):
    return db.query(DBAuthor).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
    return db.query(DBAuthor).filter(DBAuthor.id == author_id).first()


def get_author_by_name(db: Session, name: str):
    return db.query(DBAuthor).filter(DBAuthor.name == name).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_books_list(
        db: Session,
        author_id: int | None = None,
        skip: int | None = None,
        limit: int | None = None,
):

    queryset = db.query(DBBook)

    if author_id:
        queryset = queryset.filter(DBBook.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
